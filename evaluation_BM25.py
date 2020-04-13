import csv

from sklearn.metrics import ndcg_score
import pandas as pd
import pickle
from whoosh.scoring import BM25F
import numpy as np

from search import search_bm25f_and, search_single_field, search_bm25f_or

queries = pd.read_csv('./data/queries.csv')
queries = queries['query'].tolist()
queries = [item.strip() for item in queries]

with open('./data/qrels_dict.pickle', 'rb') as handle:
    qrels = pickle.load(handle)

# First count the number of relevant tables in corpus for each query.
num_of_relevant_tables = {}
for query_index, query_string in enumerate(queries):
    qrels_one_query = qrels[query_index + 1]
    num_of_relevant_tables[query_string] = 0
    for t in qrels_one_query:
        if(qrels_one_query[t] > 0):
            num_of_relevant_tables[query_string] += 1

def evaluate(search_function, scoring_function):
    """ Evaluates a search function using scoring function. See search.py for different search functions. """

    # Initialize metrics at zero.
    total_ndcg_5, total_ndcg_10, total_ndcg_15, total_ndcg_20, \
    total_prec_25, total_prec_50, total_prec_75, total_prec_100, \
    total_rec_25, total_rec_50, total_rec_75, total_rec_100 = \
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    for query_index, query_string in enumerate(queries):
        qrels_one_query = qrels[query_index + 1]

        # Execute the search function with query, scoring function.
        results, searcher = search_function(query_string, scoring_function)

        # Holds the number of relevant tables retrieved until i'th position.
        num_relevant_tables_retrieved = [0]
        num_results = 0 # Will count number of results that have annotation.
        predicted_relevance, actual_relevance = [], []

        for i, table in enumerate(results):

            if(table['id'] in qrels_one_query):
                num_results += 1
                predicted_relevance.append(table.score)
                actual_relevance.append(qrels_one_query[table['id']])

                last_num_of_relevant_tables = num_relevant_tables_retrieved[
                    len(num_relevant_tables_retrieved) - 1]
                # If table was indeed relevant, increment with 1.
                if(qrels_one_query[table['id']] > 0):
                    num_relevant_tables_retrieved.append(
                        last_num_of_relevant_tables + 1)
                else:
                    num_relevant_tables_retrieved.append(
                        last_num_of_relevant_tables
                    )
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

            # Calculate number of relevant tables at 4 levels.
            num_relevant_tables_25 = num_relevant_tables_retrieved[int(0.25 * len(num_relevant_tables_retrieved))]
            num_relevant_tables_50 = num_relevant_tables_retrieved[int(0.50 * len(num_relevant_tables_retrieved))]
            num_relevant_tables_75 = num_relevant_tables_retrieved[int(0.75 * len(num_relevant_tables_retrieved))]
            num_relevant_tables_100 = num_relevant_tables_retrieved[len(num_relevant_tables_retrieved) - 1]

            # Calculate precision at 4 levels. See slides first week.
            total_prec_25 += num_relevant_tables_25 / num_results
            total_prec_50 += num_relevant_tables_50 / num_results
            total_prec_75 += num_relevant_tables_75 / num_results
            total_prec_100 += num_relevant_tables_100 / num_results

            # Calculate recall at 4 leve ls. See slides first week.
            num_relevant_in_corpus = num_of_relevant_tables[query_string]
            if num_relevant_in_corpus > 0:
                total_rec_25 += num_relevant_tables_25 / num_relevant_in_corpus
                total_rec_50 += num_relevant_tables_50 / num_relevant_in_corpus
                total_rec_75 += num_relevant_tables_75 / num_relevant_in_corpus
                total_rec_100 += num_relevant_tables_100 / num_relevant_in_corpus

    # TODO: Divide by 60 correct?
    return \
        total_ndcg_5 / 60, total_ndcg_10 / 60, total_ndcg_15 / 60, total_ndcg_20 / 60, total_prec_25 / 60, total_prec_50 / 60, total_prec_75 / 60, total_prec_100 / 60, total_rec_25 / 60, total_rec_50 / 60, total_rec_75 / 60, total_rec_100 / 60

def hyper_parameter_evaluate():
    ks = [0.25, 0.75, 1.25, 2]
    bs = [i / 10 for i in range(11)]
    with open('ndcg_bm25_single.csv', 'w') as file:
        csv_writer = csv.writer(file)
        for k in ks:
            # Single-field BM25
            scoring_function = BM25F(K1 = k)
            search_function = search_single_field
            result = evaluate(search_function, scoring_function)
            # for titles_b in bs:
            #     for caption_and_headers_b in bs:
            #         for body_b in bs:
            #             # BM25F
            #             scoring_function = BM25F(
            #                 K1 = k,
            #                 titles_B = titles_b,
            #                 caption_and_headers_B = caption_and_headers_b,
            #                 body_B = body_b)
            #             search_function = search_bm25f_or
            #             result = evaluate(search_function, scoring_function)
            row = [k, result]
            csv_writer.writerow(row)
            print(row)

# Do the evaluation.
hyper_parameter_evaluate()