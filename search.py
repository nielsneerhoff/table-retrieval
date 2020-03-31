from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh.query import *
from whoosh.fields import *

schema = Schema(id=TEXT(stored=True), title=TEXT(stored=True), numCols=NUMERIC(stored=True), pgTitle=TEXT(stored=True), numDataRows=NUMERIC(stored=True), secondTitle=TEXT(stored=True), numHeaderRows=NUMERIC(stored=True), caption=TEXT(stored=True), content=TEXT(stored=True))

ix = open_dir("index")
mparser = MultifieldParser(["title", "content", "pgTitle", "caption", "secondTitle"], schema=schema)

with ix.searcher() as searcher:
    querystring = "fast cars"
    myquery = mparser.parse(querystring)

    results = searcher.search(myquery, limit=30)
    print(len(results))
    for i in results:
        print(i['id'])

