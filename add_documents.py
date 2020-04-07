import json

from whoosh.index import open_dir

from index import create_index, INDEX_NAME
from schema import to_fields, SCHEMA

create_index(INDEX_NAME, SCHEMA)

filename = './data/relevant_Tables_working.json'

index = open_dir(INDEX_NAME)
writer = index.writer()

with open(filename, 'r') as file:
    data = json.load(file)
    for identifier in data:
        print(identifier)
        table = data[identifier]
        fields = to_fields(identifier, table)
        writer.add_document(**fields)
writer.commit()