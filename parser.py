from whoosh.qparser import MultifieldParser, OrGroup

from schema import SCHEMA

# For single-field BM25
SINGLE_FIELD_PARSER = MultifieldParser(["all_concatenated"], schema = SCHEMA)

# For BM25F
MULTI_FIELD_PARSER = MultifieldParser(
    ['titles', 'caption_and_headers', 'body'], schema = SCHEMA, group = OrGroup)

DEFAULT_FIELD_PARSER = MultifieldParser(
    ["headers", "body", "page_title", "caption", "section_title"], schema = SCHEMA, group = OrGroup)