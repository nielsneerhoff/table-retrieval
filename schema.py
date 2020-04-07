from whoosh.fields import TEXT, NUMERIC, Schema
from whoosh.index import open_dir

SCHEMA = Schema(
    id = TEXT(stored=True),
    title = TEXT(stored=True),
    numCols = NUMERIC(stored=True),
    pgTitle = TEXT(stored=True),
    numDataRows = NUMERIC(stored=True),
    secondTitle = TEXT(stored=True),
    numHeaderRows = NUMERIC(stored=True),
    caption = TEXT(stored=True),
    content = TEXT(stored=True),
    titles = TEXT(stored=True),
    caption_and_headers = TEXT(stored=True),
    cells = TEXT(stored=True),
    all_concatenated = TEXT(stored = True))

def to_fields(identifier, table):
    fields = {}

    # TODO: Strip fields from array signs etc ?

    # Text values.
    fields['title'] = str(table['title'])
    fields['pgTitle'] = str(table['pgTitle'])
    fields['secondTitle'] = str(table['secondTitle'])
    fields['caption'] = str(table['caption'])
    fields['content'] = str(table['data'])
    fields['titles'] = fields['pgTitle'] + ' ' + fields['title']
    fields['caption_and_headers'] = fields['caption'] + ' ' # TODO
    fields['cells'] = '' # TODO
    fields['all_concatenated'] = fields['titles'] + fields['caption_and_headers'] + fields['cells']
    
    # Numeric values.
    fields['id'] = identifier
    fields['numDataRows'] = int(table['numDataRows'])
    fields['numCols'] = int(table['numCols'])
    fields['numHeaderRows'] = int(table['numHeaderRows'])

    return fields