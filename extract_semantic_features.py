import pandas as pd
import re
import json
import requests
import time

import numpy as np
import xmltodict as xml

from in_out import InOut as IO

from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

base_path_dicts = './data/dictionaries/'


def extract_semantic_features(query, table, model, key_pretex='', is_words=True, add_categories=False):
    """ Extract the semantic features with word2vec and rdf2vec
    :param query: string with query
    :param table: table json object
    """

    zeros = {
        key_pretex + 'sim' : 0,
        key_pretex + 'avg' : 0, 
        key_pretex + 'max' : 0, 
        key_pretex + 'sum' : 0
    }
    
    if is_words:
        if len(query['all_words']) == 0 or len(table['all_words']) == 0:
            return zeros

        query_words = list(filter(lambda y: y in model.keys(), query['all_words']))
        query_tfidf = list(map(lambda x: query[x]['TFIDF'], query_words))
        query_2vec = list(map(lambda x: model[x], query_words))

        table_words = list(filter(lambda y: y in model.keys(), table['all_words']))
        table_tfidf = list(map(lambda x: table[x]['TFIDF'], table_words))
        table_2vec = list(map(lambda x: model[x], table_words))

    else:
        if len(query['all_entities']) == 0 or len(table['all_entities']) == 0:
            return zeros

        query_entities = list(filter(lambda y: y in model.keys(), query['all_entities']))
        query_2vec = list(map(lambda x: model[x]['vector'], query_entities))
        if add_categories:
            query_2vec += [category for entity in query_entities for category in model[entity]['categories'].values()]
        query_tfidf = None

        table_entities = list(filter(lambda y: y in model.keys(), table['all_entities']))
        table_2vec = list(map(lambda x: model[x]['vector'], table_entities))
        if add_categories:
            table_2vec += [category for entity in table_entities for category in model[entity]['categories'].values()]
        table_tfidf = None

    if len(query_2vec) == 0 or len(table_2vec) == 0:
        return zeros

    lf_mean, lf_max, lf_sum = get_late_fusion(query_2vec, table_2vec)
    return {
        key_pretex + 'sim' : get_early_fusion(query_2vec, table_2vec, query_tfidf, table_tfidf, is_words),
        key_pretex + 'avg' : lf_mean, 
        key_pretex + 'max' : lf_max, 
        key_pretex + 'sum' : lf_sum
    }


def set_representation(content, representation='words', rdf2vec_large=None):
    """ The “raw” content of a query/table is represented as a set of terms, 
    where terms can be either words or entities.
    :param content: either the table with data or a single string
    :param representation: 'words' or 'entities'
    """
    if representation == 'words':
        if isinstance(content, str):
            content_set = list(map(lambda x: x.lower(), get_words_regex(content).split()))
        else:
            content_list = get_words_regex(content['pgTitle']).split()
            for t in content['title']:
                content_list += get_words_regex(t).split()
            content_list += get_words_regex(content['secondTitle']).split()
            content_list += get_words_regex(content['caption']).split()
            content_set = list(map(lambda x: x.lower(), content_list))

    if representation == 'entities':
        if isinstance(content, str):
            lemmatized_content = ' '.join([lemmatizer.lemmatize(word) for word in content.split()])
            content_set = set(get_entities_api(lemmatized_content)) | set(get_entities_n_grams(content, rdf2vec_large))
        else:
            max_entities_col = get_entities_core_column(content['data'], content['title'], get_entities_regex)
            entities_caption_title = get_entities_regex(content['caption'] + ' ' + content['pgTitle'])
            content_set = set(entities_caption_title).union(
                set(max_entities_col), 
                set(get_entities_n_grams(content['pgTitle'], rdf2vec_large)),
                set(get_entities_n_grams(content['caption'], rdf2vec_large))
            )
            
            content_set = content_set | {ent for header in content['title'] for ent in get_entities_n_grams(header, rdf2vec_large)}
            content_set = content_set | {ent for row in content['data'] for cell in row for ent in get_entities_n_grams(cell, rdf2vec_large)}
            
    return content_set
    


def get_entities_api(text):
    """ Retrieve list entities from text using the DBpedia API
    returns list of entities
    """
    entities = []
    param = {'text' : text}
    header = {'accept' : 'application/json'}
    url='http://api.dbpedia-spotlight.org/en/candidates'
    r = requests.get(url = url, params=param)
    print(text)
    time.sleep(1)
    if r.status_code != 200:
        print('Sleeping API for', text)
        time.sleep(5)
        return get_entities_api(text)
    content = xml.parse(r.content)
    content = json.loads(json.dumps(content))
    if 'surfaceForm' in content['annotation'].keys():
        if isinstance(content['annotation']['surfaceForm'], list):
            entities = [name['resource']['@uri'].lower() for name in content['annotation']['surfaceForm']]
        else:
            entities = [content['annotation']['surfaceForm']['resource']['@uri'].lower()]
    return entities


def get_entities_n_grams(text, rdf2vec_large):
    """Retrieves entities by matching n_grams to rdf2vec data
    
    :param text: query
    :param rdf2vec_large: rdf2vec database
    :return: list of n-gram entities
    """
    n_grams = get_n_grams(text)
    entities = [n_gram for n_gram in n_grams if n_gram in rdf2vec_large.keys()]
    return entities


def get_words_regex(text):
    """ Return string without entities using Regex
    returns string
    """
    for s in re.findall('(\[.*?\|.*?\])', text):
        text = text.replace(s, s.split('|')[1].split(']')[0])
    return text


def get_entities_regex(text):
    """ Retrieve list of entities from text using Regex
    returns list of entities
    """
    return list(map(lambda x: x.split('|')[0].lower(), re.findall('(?<=\[).*?(?=\])', text)))



def get_entities_core_column(data, title, getter):
    """ Retrieve core column with highest percentage of cells with an entity
    """
    if len(data) == 0 and len(title) == 0:
        return []
    number_of_columns = len(title)
    entities_in_column = []
    no_entities_in_column = [0] * number_of_columns
    for i, header in enumerate(title):
        entities_in_column.append(getter(header))
        if len(getter(header)) > 0:
            no_entities_in_column[i] += 1
    for row in data:
        for i, val in enumerate(row):
            entities_in_column[i] += getter(val)
            if len(getter(val)) > 0:
                no_entities_in_column[i] += 1
    return entities_in_column[no_entities_in_column.index(max(no_entities_in_column))]


def get_centroid(arr, tfidf, is_words):
    nparr = np.array(arr)
    length, dim = nparr.shape
    if is_words:
        ret = [0] * dim
        for i, col in enumerate(arr):
            for j, cell in enumerate(col):
                ret[j] += cell * tfidf[i]
        return np.array(ret)
    else:
        return np.array([np.sum(nparr[:, i])/length for i in range(dim)])



def get_early_fusion(query_vecs, table_vecs, query_tfidf, table_tfidf, is_words):
    """ Calculate the cosine similarity between the centroid of the quary and table vectors.
    """
    return cosine_similarity(get_centroid(query_vecs, query_tfidf, is_words), get_centroid(table_vecs, table_tfidf, is_words))



def get_late_fusion(query, table):
    """ Calculate the cosine similarity between all vector pairs between query and table and 
    return the mean, max and sum 
    """
    pairs = np.zeros(len(query) * len(table))
    for i, q in enumerate(query):
        for j, t in enumerate(table):
            pairs[i * len(table) - 1 + j] = cosine_similarity(q ,t)
    return pairs.mean(), pairs.max(), pairs.sum()


def cosine_similarity(X, Y):
    return np.dot(X, Y) / (np.linalg.norm(X) * np.linalg.norm(Y))


def get_n_grams(query):
    n_grams = []
    split = query.split()
    for i in range(len(split)):
        j = i + 1
        while j <= len(split):
            n_gram = '_'.join(split[i:j])
            n_grams.append(n_gram)
            j += 1
    return n_grams