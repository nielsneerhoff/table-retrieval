import pandas as pd
import json
from os import listdir

files = listdir("C:/Users/wybek/Documents/school/Master/Information Retrieval/proproceed/tables_redi2_1/")


answers = pd.read_csv('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/qrels.txt', sep='\t', names=['Query', 'something', 'id', 'relevance'])
id = answers['id'].tolist()
id_dict = dict(zip(id, id))
print(len(id_dict))
total_ids_found = 0

for file in files:
    print(file)
    with open("C:/Users/wybek/Documents/school/Master/Information Retrieval/proproceed/tables_redi2_1/" + file) as json_file:
        data = json.load(json_file)
        tables = {}
        for i in data:
            if i in id_dict:
                print("Found id: " + str(id_dict[i]))
                total_ids_found +=1
                tables[i] = []
                tables[i].append(data[i])
print(total_ids_found)
with open('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/relevant_Tables.json', 'w') as outfile:
    json.dump(tables, outfile)

