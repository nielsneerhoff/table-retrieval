from whoosh import scoring
from whoosh import searching

from index import INDEX
from parser import SINGLE_FIELD_PARSER, MULTI_FIELD_PARSER

def BM25F(titles_b, caption_and_headers_b, cells_b):
    """ Returns a BM25F scoring function with B parameter configuration specified in arguments. """

    return scoring.BM25F(
        titles_B = titles_b,
        cells_b = cells_b,
        caption_and_headers_b = caption_and_headers_b
    )

# Dummy bm25f scoring function with trivial weights.
DUMMY_BM25F = BM25F(1, 1, 1)

def search(query_string, scoring_function, query_parser, index = INDEX, limit = 30):
    """ Search index using a scoring function and a query parser. Limits search results to limit. """

    with index.searcher(weighting = scoring_function) as searcher:
        query = query_parser.parse(query_string)
        results = searcher.search(query, limit=30)
        print(len(results), 'results found for', query_string)
        return results

def search_bm25f(query_string, scoring_function, index = INDEX, limit = 30):
    """ Search index using bm25f scoring function and composite multi-field parser. Limits search results to limit. """

    return search(query_string, scoring_function, MULTI_FIELD_PARSER)

def search_single_field(
    query_string, scoring_function, index = INDEX, limit = 30):
    """ Search index using bm25f scoring function and composite multi-field parser. Limits search results to limit. """

    return search(query_string, scoring_function, SINGLE_FIELD_PARSER)

def search_multi_field(
    query_string, scoring_function, index = INDEX, limit = 30):
    """ Search index using bm25f scoring function and multi-field parser. Limits search results to limit. """

    # To be implemented.
    pass
