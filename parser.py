from whoosh.qparser import MultifieldParser, OrGroup

from schema import SCHEMA

# For single-field BM25
SINGLE_FIELD_PARSER = MultifieldParser(["all_concatenated"], schema = SCHEMA)

# For BM25F
MULTI_FIELD_PARSER = MultifieldParser(
    ['titles', 'caption_and_headers', 'cells'], schema = SCHEMA, group = OrGroup)

DEFAULT_FIELD_PARSER = MultifieldParser(
    ["title", "content", "pgTitle", "caption", "secondTitle"], schema = SCHEMA, group = OrGroup)