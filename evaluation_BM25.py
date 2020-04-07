from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh.query import *
from whoosh.fields import *
from sklearn.metrics import ndcg_score
import pandas as pd
from whoosh import scoring
import pickle
from whoosh import qparser


queries = pd.read_csv('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/queries.csv')
queries = queries['query'].tolist()
queries = [item.strip() for item in queries]

with open('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/qrels_dict.pickle', 'rb') as handle:
    qrels = pickle.load(handle)

schema = Schema(id=TEXT(stored=True), title=TEXT(stored=True), numCols=NUMERIC(stored=True), pgTitle=TEXT(stored=True), numDataRows=NUMERIC(stored=True), secondTitle=TEXT(stored=True), numHeaderRows=NUMERIC(stored=True), caption=TEXT(stored=True), content=TEXT(stored=True))

ix = open_dir("index")
mparser = MultifieldParser(["title", "content", "pgTitle", "caption", "secondTitle"], schema=schema, group=qparser.OrGroup)
total_ndcg_5 = 0
total_ndcg_10 = 0
total_ndcg_15 = 0
total_ndcg_20 = 0
for index, query in enumerate(queries):
    query_number = index + 1

    with ix.searcher(weighting=scoring.BM25F) as searcher:
        querystring = str(query)
        print(str(query_number) + " " + querystring)
        myquery = mparser.parse(querystring)

        results = searcher.search(myquery)
        print("Retrieved: " + str(len(results)) + " tables")
        qrels_one_query = qrels[query_number]

        predicted_relevance = list()
        actual_relevance = list()
        for table in results:
            #print('Table id: ' + str(table['id']) + ' BM25 score: ' + str(table.score))
            if(table['id'] in qrels_one_query):
                predicted_relevance.append(table.score)
                actual_relevance.append(qrels_one_query[table['id']])
        #print(predicted_relevance)
        #print(actual_relevance)

        if(len(actual_relevance) > 1):
            total_ndcg_5 += ndcg_score([actual_relevance], [predicted_relevance], k = 5)
            total_ndcg_10 += ndcg_score([actual_relevance], [predicted_relevance], k = 10)
            total_ndcg_15 += ndcg_score([actual_relevance], [predicted_relevance], k = 15)
            total_ndcg_20 += ndcg_score([actual_relevance], [predicted_relevance], k = 20)
            #print("ndcg: " + str(ndcg))


print("average ndcg @ 5 score = " + str(total_ndcg_5 / 60))
print("average ndcg @ 10 score = " + str(total_ndcg_10 / 60))
print("average ndcg @ 15 score = " + str(total_ndcg_15 / 60))
print("average ndcg @ 20 score = " + str(total_ndcg_20 / 60))