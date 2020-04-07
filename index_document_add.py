import json

import schema
import index

filename = './data/relevant_Tables_working.json'

with open(filename, 'r') as file:
    data = json.load(file)
    for identifier in data:
        table = data[identifier]
        fields = schema.to_fields(identifier, table)
        index.add_document(**fields)
