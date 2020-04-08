from whoosh import scoring
from whoosh import searching
from schema import SCHEMA
from whoosh.index import open_dir
from parser_2 import SINGLE_FIELD_PARSER, MULTI_FIELD_PARSER, DEFAULT_FIELD_PARSER

from index import INDEX_NAME



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
