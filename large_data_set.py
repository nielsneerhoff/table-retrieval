import pandas as pd

from re import sub
import json

# WQT.dataset.table.tsv lists tables in the dataset A table includes 
# {TableID, Source, Caption, Sub-Caption, ColumnStr, CellStr, URL}. 
# Source: WebQuery or Wiki
# ColumnStr: joined by " | "
# CellStr: Adjacent cells are joined by "_|_".
# Adjacent lines are joined by " || ".

# For example: 
# [Table]:      +----+------+
#               | ID | Name |
#               |  0 |   A  | 
#               |  1 |   B  |
#               +----+------+
# [ColumnStr]:  "ID | Name"
# [CellStr]:    "0 | A || 1 | B"

# The file (about 61 mb). Is in .gitignore.
filename = './data/wikiquery_data_utf8.tsv'

data = pd.read_csv(filename, sep="\t")
tables = {}
num_of_tables = {} # Maps a hyperlink to the number of tables on that page.
for i in range(len(data)):
    print(i)
    row = data.iloc[i]
    table = {}

    # Count the number of tables on this hyperlink.
    link = row['URL']
    num = 0
    if link in num_of_tables:
        num = num_of_tables[link]
    num_of_tables[link] = num + 1

    # Retrieve other table info.
    table_id = int(row['TableID'])
    table['link'] = link
    table['source'] = row['Source']
    table['title'] = row['Caption']
    table['sub_title'] = row['Sub-Caption']
    headers = row['ColumnStr'].split(' _|_ ')
    table['headers'] = headers
    table['num_headers'] = len(headers)
    lines = row['CellStr'].split(' _||_ ')
    table['num_rows'] = len(lines)
    content = []
    numeric_columns = set()
    for line in lines:
        line = line.split(' _|_ ')
        for k, cell in enumerate(line):
            formatted_cell = sub('[.,]', '', cell)
            if formatted_cell.isnumeric() and k not in numeric_columns:
                numeric_columns.add(k)
        content.append(line)
    table['numeric_columns'] = list(numeric_columns)
    table['data'] = content
    tables[table_id] = table

for table_id in tables:
    table = tables[table_id]
    link = table['link']
    table['num_of_tables'] = num_of_tables[link]

json_filename = './data/wikiquery_json.json'
with open(json_filename, 'w') as file:
    json.dump(tables, file)