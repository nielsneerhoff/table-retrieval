import os.path

from whoosh.index import create_in, open_dir

from schema import SCHEMA

INDEX_NAME = 'INDEX'

def create_index(index_name, schema):
    """ Creates an index storing the documents. """

    if not os.path.exists(index_name):
        os.mkdir(index_name)
    return create_in(index_name, schema)

INDEX = create_index(INDEX_NAME, SCHEMA)

def add_document(index = INDEX, **kwargs):
    """ Adds a document with fields in kwargs to index. """

    writer = index.writer()
    writer.add_document(**kwargs)
    writer.commit()
