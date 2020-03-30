import pandas as pd
import json
data = pd.read_json('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/relevant_Tables_working.json').T.reset_index()
data.to_csv('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/relevant_Tables.csv')