from sklearn.metrics import ndcg_score
import pandas as pd
import pickle

from search import search_bm25f, search_single_field, BM25F

queries = pd.read_csv('./data/queries.csv')
queries = queries['query'].tolist()
queries = [item.strip() for item in queries]

with open('./data/qrels_dict.pickle', 'rb') as handle:
    qrels = pickle.load(handle)

def evaluate(search_function, scoring_function):
    """ Evaluates a search function using scoring function. See search.py for different search functions. """
    # Initialize NDCG's at zero.
    total_ndcg_5, total_ndcg_10, total_ndcg_15, total_ndcg_20 = 0, 0, 0, 0

    for query_index, query_string in enumerate(queries):
        qrels_one_query = qrels[query_index + 1]

        # Execute the search function with query, scoring function.
        results, searcher = search_function(query_string, scoring_function)

        predicted_relevance = []
        actual_relevance = []
        for table in results:
            if(table['id'] in qrels_one_query):
                predicted_relevance.append(table.score)
                actual_relevance.append(qrels_one_query[table['id']])

        searcher.close()

        if(len(actual_relevance) > 1):
            total_ndcg_5 += ndcg_score(
                [actual_relevance], [predicted_relevance], k = 5)
            total_ndcg_10 += ndcg_score(
                [actual_relevance], [predicted_relevance], k = 10)
            total_ndcg_15 += ndcg_score(
                [actual_relevance], [predicted_relevance], k = 15)
            total_ndcg_20 += ndcg_score(
                [actual_relevance], [predicted_relevance], k = 20)

    return {
        'ndcg_at_5' : total_ndcg_5 / 60, 
        'ndcg_at_10' : total_ndcg_10 / 60,
        'ndcg_at_15' : total_ndcg_15 / 60,
        'ndcg_at_20' : total_ndcg_20 / 60
        # TODO Add MAP, and others?
        }

def hyper_parameter_evaluate():
    for i in range(1, 10):
        titles_b = i / 10
        for j in range(1, 10):
            caption_and_headers = j / 10
            for k in range(1, 10):
                cells_b = k / 10
                # BM25F
                scoring_function = BM25F(
                    titles_b, caption_and_headers, cells_b)
                search_function = search_bm25f
                # Single-field BM25
                # scoring_function = BM25F()
                # search_function = search_single_field
                result = evaluate(search_function, scoring_function)
                print(i, j, k, result)

hyper_parameter_evaluate()