import pandas as pd
import pickle




qrels = pd.read_csv('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/qrels.txt', sep='\t', names=['query', 'nothing', 'table_id', 'relevance'])
print(qrels)

all_qrels_dict = {}
for i in range(60):
    data = qrels.loc[qrels['query'] == i + 1]
    qrels_one_query = dict(zip(data.table_id, data.relevance))
    all_qrels_dict[i+1] = qrels_one_query

with open('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/qrels_dict.pickle', 'wb') as handle:
    pickle.dump(all_qrels_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

#open the pickled dict of qrels using the following file
# with open('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/qrels_dict.pickle', 'rb') as handle:
#     b = pickle.load(handle)

