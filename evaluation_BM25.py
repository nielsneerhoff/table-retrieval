from sklearn.metrics import ndcg_score
import pandas as pd
import pickle
from whoosh.index import open_dir

from search import search_bm25f, DUMMY_BM25F
from index import INDEX_NAME

INDEX = open_dir(INDEX_NAME)

queries = pd.read_csv('./data/queries.csv')
queries = queries['query'].tolist()
queries = [item.strip() for item in queries]

with open('./data/qrels_dict.pickle', 'rb') as handle:
    qrels = pickle.load(handle)

total_ndcg_5 = 0
total_ndcg_10 = 0
total_ndcg_15 = 0
total_ndcg_20 = 0
for index, query in enumerate(queries):
    query_number = index + 1
    query_string = str(query)

    results = search_bm25f(query_string, DUMMY_BM25F, INDEX)
    qrels_one_query = qrels[query_number]

    predicted_relevance = list()
    actual_relevance = list()
    for table in results:
        if(table.docnum in qrels_one_query):
            predicted_relevance.append(table.score)
            actual_relevance.append(qrels_one_query[table['id']])

    if(len(actual_relevance) > 1):
        total_ndcg_5 += ndcg_score(
            [actual_relevance], [predicted_relevance], k = 5)
        total_ndcg_10 += ndcg_score(
            [actual_relevance], [predicted_relevance], k = 10)
        total_ndcg_15 += ndcg_score(
            [actual_relevance], [predicted_relevance], k = 15)
        total_ndcg_20 += ndcg_score(
            [actual_relevance], [predicted_relevance], k = 20)


print("average ndcg @ 5 score = " + str(total_ndcg_5 / 60))
print("average ndcg @ 10 score = " + str(total_ndcg_10 / 60))
print("average ndcg @ 15 score = " + str(total_ndcg_15 / 60))
print("average ndcg @ 20 score = " + str(total_ndcg_20 / 60))