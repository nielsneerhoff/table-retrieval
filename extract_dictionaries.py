from in_out import InOut as IO
base_path_dicts = './data/dictionaries/'
from extract_semantic_features import set_representation, get_entities_regex
from math import log
import wikipedia
import numpy as np
from math import log

def create_word2vec_model(bin_model, words):
    word2vec = {}
    for word in bin_model.wv.index2word:
        if word.lower() in words:
            word2vec[word.lower()] = bin_model[word].tolist()
    IO.write_json(word2vec, base_path_dicts + 'word2vec.json')
    return word2vec

def create_rdf2vec_model(large_model, entities):
    rdf2vec = {}
    for word in large_model.keys():
        if word.lower() in entities:
            rdf2vec[word.lower()] = large_model[word]
    IO.write_json(rdf2vec, base_path_dicts + 'rdf2vec.json')
    return rdf2vec


def get_all_words(queries, tables):
    query_to_words = {}
    table_to_words = {}
    all_words = set()

    for q_id, query in queries.items():
        words_query = set_representation(query, 'words')
        query_to_words[q_id] = {'all_words' : words_query}
        all_words = all_words.union(words_query)

    for t_id, table in tables.items():
        words_table = set_representation(table, 'words')
        table_to_words[t_id] = {'all_words' : words_table}
        all_words = all_words.union(words_table)

    get_TFIDF(queries, tables, query_to_words, table_to_words)

    return all_words, query_to_words, table_to_words


def get_all_entities(queries, tables, rdf2vec_large=None):
    query_to_entities = {}
    table_to_entities = {}
    all_entities = set()

    for q_id, query in queries.items():
        entities_query = set_representation(query, 'entities', rdf2vec_large)
        query_to_entities[q_id] = {'all_entities' : list(entities_query)}
        for entity in entities_query:
            query_to_entities[q_id][entity] = {}
        all_entities = all_entities.union(entities_query)
    IO.write_json(query_to_entities, base_path_dicts + 'query_to_entities.json')


    for t_id, table in tables.items():
        entities_table = set_representation(table, 'entities', rdf2vec_large)
        table_to_entities[t_id] = {'all_entities' : list(entities_table)}
        for entity in entities_table:
            table_to_entities[t_id][entity] = {}
        all_entities = all_entities.union(entities_table)
    IO.write_json(table_to_entities, base_path_dicts + 'table_to_entities.json')

    return all_entities, query_to_entities, table_to_entities


def get_TFIDF(queries, tables, query_to_words, table_to_words):
    for q_id, query in queries.items():
        words_query = query_to_words[q_id]['all_words']
        for word in words_query:
            query_to_words[q_id][word] = {
                'TF' : len([x for x in words_query if x == word]) / len(words_query),
                'IDF' : log(len(queries) / len([word for x in query_to_words.values() if word in x['all_words']]))
                }
            query_to_words[q_id][word]['TFIDF'] = \
            query_to_words[q_id][word]['TF'] / query_to_words[q_id][word]['IDF']
            query_to_words[q_id]['all_words'] = list(set(query_to_words[q_id]['all_words']))
    IO.write_json(query_to_words, base_path_dicts + 'query_to_words.json')

    for t_id, table in tables.items():
        words_table = table_to_words[t_id]['all_words']
        for word in words_table:
            table_to_words[t_id][word] = {
                'TF' : len([x for x in words_table if x == word]) / len(words_table),
                'IDF' : log(len(tables) / len([word for x in table_to_words.values() if word in x['all_words']]))
                }
            table_to_words[t_id][word]['TFIDF'] = \
            table_to_words[t_id][word]['TF'] / table_to_words[t_id][word]['IDF']
            table_to_words[t_id]['all_words'] = list(set(table_to_words[t_id]['all_words']))
    IO.write_json(table_to_words, base_path_dicts + 'table_to_words.json')


def get_all_words_from_json(query_to_words, table_to_words):
    all_words = set()
    for query in query_to_words.values():
        all_words = all_words.union(query['all_words'])
    for table in table_to_words.values():
        all_words = all_words.union(table['all_words'])
    return all_words


def get_all_entities_from_json(query_to_entities, table_to_entities):
    all_entities = set()
    for query in query_to_entities.values():
        all_entities = all_entities.union(query['all_entities'])
    for table in table_to_entities.values():
        all_entities = all_entities.union(table['all_entities'])
    return all_entities


def compute_query_to_idfs(query_to_words, tables):
    """Calculate IDFs of the queries
    idf1 : IDF page title : pgTitle
    idf2 : IDF section title : secondTitle
    idf3 : IDF table caption : caption
    idf4 : IDF table heading : title
    idf5 : IDF table body : body
    idf6 : IDF "catch-all" : sum of the above
    
    :param query_to_words: query to words dictionary
    :param tables: tables dictionary

    IDF_f (q) = sum_t∈q IDF_f (t)
    IDF_f (t) = log(N / (# docs where t occurs in field f = n_t))
    """    
    query_to_idfs = {}
    N = len(tables)
    for q, query in query_to_words.items():
        query_to_idfs[q] = {
            'idf1' : 0, 'idf2' : 0, 'idf3' : 0, 'idf4' : 0, 'idf5' : 0, 'idf6' : 0
        }
        for word in query['all_words']:
            n_t1 = 0; n_t2 = 0; n_t3 = 0; n_t4 = 0; n_t5 = 0
            for i, table in tables.items():
                if word in table['pgTitle'].split(): n_t1 += 1
                if word in table['secondTitle'].split(): n_t2 += 1
                if word in table['caption'].split(): n_t3 += 1
                if word in ' '.join(table['title']).split(): n_t4 += 1
                if word in ' '.join([cell for row in table['data'] for cell in row]).split(): n_t5 += 1
            n_t6 = sum([n_t1, n_t2, n_t3, n_t4, n_t5])
            if n_t1 > 0: query_to_idfs[q]['idf1'] += log(N / n_t1)
            if n_t2 > 0: query_to_idfs[q]['idf2'] += log(N / n_t2)
            if n_t3 > 0: query_to_idfs[q]['idf3'] += log(N / n_t3)
            if n_t4 > 0: query_to_idfs[q]['idf4'] += log(N / n_t4)
            if n_t5 > 0: query_to_idfs[q]['idf5'] += log(N / n_t5)
            if n_t6 > 0: query_to_idfs[q]['idf6'] += log(N / n_t6)
    IO.write_json(query_to_idfs, base_path_dicts + 'query_to_idfs.json')
    return query_to_idfs


def extend_queries_with_rdf2vec_categories(queries, rdf2vec_large):
    """Add categories of entities to queries
    
    :param queries: The current queries under investigation
    :param rdf2vec_large: rdf2vec model
    """    
    extended_queries = {}
    for q_id, query in queries.items():
        categories = []
        entities = list(filter(lambda y: y in rdf2vec_large.keys(), set_representation(query, 'entities', rdf2vec_large)))
        categories = [category for entity in entities for category in rdf2vec_large[entity]['categories'].keys()]
        extended_queries[q_id] = query + ' ' + ' '.join(categories)
    IO.write_json(extended_queries, base_path_dicts + 'extended_queries.json')
    return extended_queries