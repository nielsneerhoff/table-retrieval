import pandas as pd
import re
import json
import requests
import numpy as np
from in_out import InOut as IO

base_path_dicts = './data/dictionaries/'


def extract_semantic_features(query, table, model, early_fusion=True, is_words=True):
    """ Extract the semantic features with word2vec and rdf2vec
    :param query: string with query
    :param table: table json object
    """
    
    if is_words:
        if len(query['all_words']) == 0 or len(table['all_words'] == 0):
            return -1
        query_words = list(filter(lambda y: y in model.keys(), query['all_words']))
        query_tfidf = list(map(lambda x: query[x]['TFIDF'], query_words))
        query_2vec = list(map(lambda x: model[x], query_words))

        table_words = list(filter(lambda y: y in model.keys(), table['all_words']))
        table_tfidf = list(map(lambda x: table[x]['TFIDF'], table_words))
        table_2vec = list(map(lambda x: model[x], table_words))
    else:
        if len(query['all_entities']) == 0 or len(table['all_entities'] == 0):
            return -1
        query_2vec = list(map(lambda x: model[x], list(filter(lambda y: y in model.keys(), query['all_entities']))))
        table_2vec = list(map(lambda x: model[x], list(filter(lambda y: y in model.keys(), table['all_entities']))))

    if early_fusion:
        return get_early_fusion(query_2vec, table_2vec, query_tfidf, table_tfidf, is_words)
    else:
        return get_late_fusion(query_2vec, table_2vec)



def set_representation(content, representation='words'):
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
            content_set = set(get_entities_api(content))
        else:
            max_entities_col = get_entities_core_column(content['data'], content['title'], get_entities_regex)
            entities_caption_title = get_entities_regex(content['caption'] + ' ' + content['pgTitle'])
            content_set = set(entities_caption_title).union(set(max_entities_col))
    
    return content_set
    


def get_entities_api(text):
    """ Retrieve list entities from text using the DBpedia API
    returns list of entities
    """
    entities = []
    param = { 'text' : text }
    url='http://api.dbpedia-spotlight.org/en/candidates'
    r = requests.get(url = url, params=param) 
    if r.status_code != 200:
        raise ConnectionError
        return print('Error API')
    content = json.loads(r.content)
    if 'surfaceForm' in content['annotation'].keys():
        if isinstance(content['annotation']['surfaceForm'], list):
            entities = [name['@name'] for name in content['annotation']['surfaceForm']]
        else:
            entities = [content['annotation']['surfaceForm']['@name']]
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


def get_centroid(arr, tfidf=None, is_words=True):
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



def get_early_fusion(query_vecs, table_vecs, query_tfidf, table_tfidf, is_words=True):
    """ Calculate the cosine similarity between the centroid of the quary and table vectors.
    """
    if is_words:
        return cosine_similarity(get_centroid(query_vecs, query_tfidf, is_words), get_centroid(table_vecs, table_tfidf, is_words))
    else:
        return cosine_similarity(get_centroid(query_vecs), get_centroid(table_vecs))



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