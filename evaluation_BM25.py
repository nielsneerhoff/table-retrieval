from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh.query import *
from whoosh.fields import *
from sklearn.metrics import ndcg_score
import pandas as pd
from whoosh import scoring


queries = pd.read_csv('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/queries.csv')
queries = queries['query'].tolist()
queries = [item.strip() for item in queries]

qrels = pd.read_csv('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/qrels.txt', sep='\t', names=['query', 'nothing', 'table_id', 'relevance'])
rel_ids_1 = qrels[['table_id', 'relevance']].head(60)
print(rel_ids_1)

schema = Schema(id=TEXT(stored=True), title=TEXT(stored=True), numCols=NUMERIC(stored=True), pgTitle=TEXT(stored=True), numDataRows=NUMERIC(stored=True), secondTitle=TEXT(stored=True), numHeaderRows=NUMERIC(stored=True), caption=TEXT(stored=True), content=TEXT(stored=True))

ix = open_dir("index")
mparser = MultifieldParser(["title", "content", "pgTitle", "caption", "secondTitle"], schema=schema)

with ix.searcher(weighting=scoring.BM25F) as searcher:
    querystring = "fast cars"
    myquery = mparser.parse(querystring)

    results = searcher.search(myquery, limit=60)
    print(len(results))
    for i in results:
        print('Table id: ' + str(i['id']) + ' BM25 score: ' + str(i.score))

