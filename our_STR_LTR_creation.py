import pandas as pd
import pickle

data = pd.read_csv('./data/Berend_Final.csv', index_col=0)

with open('./data/qrels_dict.pickle', 'rb') as handle:
    qrels = pickle.load(handle)


qrels_list = list()
for index, row in data.iterrows():
    qrels_1_query = qrels[row['query_id']]
    qrels_list.append(qrels_1_query[row['table_id']])

print(qrels_list)

data['rel'] = qrels_list

print(data)
data.to_csv('./data/Berend_version_1_with_rels.csv')
data = data.drop(['query'], axis=1)

STR = data

LTR = data.drop(['esim', 'eavg', 'esum', 'resim', 'reavg', 'remax', 'resum', 'emax'], axis=1)
print(STR)
print(LTR)

LTR.to_csv('./data/Our_LTR.csv')
STR.to_csv('./data/Our_STR.csv')