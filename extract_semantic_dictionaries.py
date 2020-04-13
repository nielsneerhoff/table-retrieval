from in_out import InOut as IO
base_path_dicts = './data/dictionaries/'
from extract_semantic_features import set_representation, get_entities_regex
from math import log
import wikipedia

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


def get_all_entities(queries, tables):
    query_to_entities = {}
    table_to_entities = {}
    all_entities = set()

    for q_id, query in queries.items():
        # entities_query = find_all_entities_in_query(query)
        entities_query = set_representation(query, 'entities')
        query_to_entities[q_id] = {'all_entities' : list(entities_query)}
        for entity in entities_query:
            query_to_entities[q_id][entity] = {}
        all_entities = all_entities.union(entities_query)
    IO.write_json(query_to_entities, base_path_dicts + 'query_to_entities.json')


    for t_id, table in tables.items():
        entities_table = set_representation(table, 'entities')
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


# def find_all_entities_in_query(query):
#     query_to_ngrams = {}

#     splitted = query.split(' ')
#     query_to_ngrams[splitted[0]] = list_to_ngrams(splitted[1:])

#     query_to_entities = {}
#     entities = []

#     for k, v in query_to_ngrams.items():
#         query_entities = [check_if_entity(i) for i in v if check_if_entity(i) is not None]
#         query_to_entities[k] = sorted(list(set(query_entities)))
#         entities += query_entities

#     return entities, query_to_entities


# def check_if_entity(s):
#     try:
#         page = wikipedia.page(s)
#         res = page.url.split('/')[-1]
#         if res.lower().replace('_', ' ') == s:
#             return res
#         else:
#             return
#     except wikipedia.PageError:
#         return
#     except wikipedia.DisambiguationError:
#         return


# def list_to_ngrams(words):
#     words_incl_n_grams = []
#     for N in range(1, len(words) + 1):
#         words_incl_n_grams += [' '.join(words[i:i+N]).strip() for i in range(len(words)-N+1)]
#     return words_incl_n_grams
