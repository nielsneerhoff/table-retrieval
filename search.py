from whoosh import scoring
from whoosh import searching
from whoosh.index import open_dir

from index import INDEX_NAME
from parser import SINGLE_FIELD_PARSER, MULTI_FIELD_PARSER, DEFAULT_FIELD_PARSER

def BM25F(titles_b, caption_and_headers_b, cells_b):
    """ Returns a BM25F scoring function with B parameter configuration specified in arguments. """

    return scoring.BM25F(
        titles_B = titles_b,
        cells_b = cells_b,
        caption_and_headers_b = caption_and_headers_b
    )

def BM25F():
    """ Returns a default BM25F scoring function. """

    return scoring.BM25F()

def search(query_string, scoring_function, query_parser, index_name):
    """ Search index using a scoring function and a query parser. Limits search results to limit. """

    try:
        index = open_dir(index_name)
        searcher = index.searcher(weighting = scoring_function)
        query = query_parser.parse(query_string)
        results = searcher.search(query, limit = 3120)
    finally:
        return results, searcher

def search_bm25f(query_string, scoring_function, index_name = INDEX_NAME):
    """ Search index using bm25f scoring function and composite multi-field parser. Limits search results to limit. """

    return search(query_string, scoring_function, MULTI_FIELD_PARSER, index_name)

def search_single_field(query_string, scoring_function, index_name = INDEX_NAME):
    """ Search index using bm25f scoring function and composite multi-field parser. Limits search results to limit. """

    return search(query_string, scoring_function, SINGLE_FIELD_PARSER, index_name)

def search_multi_field(query_string, scoring_function, index_name = INDEX_NAME):
    """ Search index using bm25f scoring function and multi-field parser. Limits search results to limit. """

    # TODO To be implemented. After call David Maxwell.
    pass