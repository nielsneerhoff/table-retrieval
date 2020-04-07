from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh.query import *
from whoosh.fields import *

from schema import schema

ix = open_dir("index")
mparser = MultifieldParser(["title", "content", "pgTitle", "caption", "secondTitle"], schema=schema)

with ix.searcher() as searcher:
    querystring = "fast cars"
    myquery = mparser.parse(querystring)

    results = searcher.search(myquery, limit=30)
    print(len(results))
    for i in results:
        print(i['id'])

