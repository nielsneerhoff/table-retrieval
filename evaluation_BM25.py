import csv

from sklearn.metrics import ndcg_score
import pandas as pd
import pickle
from whoosh.scoring import BM25F

from search import search_bm25f_and, search_single_field

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

    return total_ndcg_5 / 60, total_ndcg_10 / 60, total_ndcg_15 / 60, total_ndcg_20 / 60

def hyper_parameter_evaluate():
    ks = [25, 50, ]
    with open('ndcg_bm25.csv', 'w') as file:
        csv_writer = csv.writer(file)
        for k in range(25, 201, 25):
            k = k / 100
            # Single-field BM25
            scoring_function = BM25F(K1 = k)
            search_function = search_single_field
            result = evaluate(search_function, scoring_function)
            for tb in range(11):
                titles_b = tb / 10
                for cb in range(11):
                    caption_and_headers_b = cb / 10
                    for bb in range(11):
                        body_b = bb / 10
                        # BM25F
                        scoring_function = BM25F(
                            K1 = k, 
                            titles_B = titles_b,
                            caption_and_headers_B = caption_and_headers_b,
                            body_B = body_b)
                        search_function = search_bm25f_and
                        result = evaluate(search_function, scoring_function)
                        row = [k, titles_b, caption_and_headers_b, body_b, result]
                        csv_writer.writerow(row)
                        print(row)

# Do the evaluation.
hyper_parameter_evaluate()