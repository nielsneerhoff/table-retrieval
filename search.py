from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.query import *

ix = open_dir("index")

with ix.searcher() as searcher:
    querystring = 'world interest rates table'
    myquery = Term("content", u"cars")

    results = searcher.search(myquery)
    print(len(results))
    print(results[0])

