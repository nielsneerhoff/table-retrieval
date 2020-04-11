import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold
import pickle
from sklearn.metrics import ndcg_score

#
#features_file = pd.read_csv('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/LTR_features.csv', index_col=0)
features_file = pd.read_csv('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/STR_features.csv', index_col=0)
features_file = features_file.set_index('table_id')

#load the qrels dictionary
with open('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/qrels_dict.pickle', 'rb') as handle:
    qrels = pickle.load(handle)

regression_model = RandomForestRegressor(n_estimators=1000, max_leaf_nodes=4)

#get a list from 1 to 60 which will be split up for k fold cross validation
queries = features_file['query_id'].drop_duplicates()
queries = queries.tolist()

kf = KFold(n_splits=5, random_state=2, shuffle=True)

total_ndcg_5, total_ndcg_10, total_ndcg_15, total_ndcg_20 = 0, 0, 0, 0

for train_index, test_index in kf.split(queries):
    #get the features for the rows that match the query and fit the model
    X = features_file.loc[features_file['query_id'].isin(train_index)]
    Y = features_file.loc[features_file['query_id'].isin(train_index)]
    X = X.drop(labels='rel', axis = 1)
    Y = Y['rel']
    regression_model.fit(X.iloc[:, 1:], Y)

    #in this loop I evaluate the ndcg score for every query in the validation dataset
    for query_id in test_index:
        query_id_actual = query_id + 1
        tables_one_query = features_file.loc[features_file['query_id'] == query_id_actual]
        tables_one_query = tables_one_query.drop(labels=['query_id', 'rel'], axis = 1)

        results = regression_model.predict(tables_one_query)
        table_id_and_rankings = pd.DataFrame([tables_one_query.index, results]).T
        table_id_and_rankings.columns = ['table_id', 'ranking']
        table_id_and_rankings = table_id_and_rankings.sort_values(by=['ranking'], axis=0, ascending=False)
        qrels_one_query = qrels[query_id_actual]

        actual_relevance = list()
        predicted_relevance = list()
        for index, row in table_id_and_rankings.iterrows():
            if(row['table_id'] in qrels_one_query):
                actual_relevance.append(qrels_one_query[row['table_id']])
                predicted_relevance.append(row['ranking'])
        total_ndcg_5 += ndcg_score(
            [actual_relevance], [predicted_relevance], k=5)
        total_ndcg_10 += ndcg_score(
            [actual_relevance], [predicted_relevance], k=10)
        total_ndcg_15 += ndcg_score(
            [actual_relevance], [predicted_relevance], k=15)
        total_ndcg_20 += ndcg_score(
            [actual_relevance], [predicted_relevance], k=20)

print(total_ndcg_5 / 60, total_ndcg_10 / 60, total_ndcg_15 / 60, total_ndcg_20 / 60)