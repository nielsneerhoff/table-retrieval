from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from whoosh import scoring

from schema import schema

def BM25F(titles_B, caption_and_header_B, content_B):
    """ Returns a BM25F scoring function with B parameter configuration specified in arguments. """

    # TODO: Match to fields that we will use.
    # TODO: Set to appropriate values ???.
    return scoring.BM25F(
        title_B = 0.25,
        pgTitle_B = 0.25,
        caption_B = 0.25,
        content_B = 0.25
    )

# Dummy bm25f scoring function.
bm25f = BM25F(0, 0, 0)
# Default index.
index = open_dir("index")
# Default query parser.
multi_field_parser = MultifieldParser(
    ["title", "content", "pgTitle", "caption", "secondTitle"], 
    schema = schema)

def search(
    scoring_function = bm25f, query_parser = multi_field_parser, index = index, limit = 30):
    """ Search index using a scoring function and a query parser. Limits search results to limit. """

    with index.searcher(weighting = scoring_function) as searcher:
        query_string = "fast cars"
        query = query_parser.parse(query_string)
        results = searcher.search(query, limit = 30)
        print(len(results))
        for i in results:
            print(i['id'])
        return results