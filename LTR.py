import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold
import pickle
from sklearn.metrics import ndcg_score

#features from OG data
#features_file = pd.read_csv('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/LTR_features.csv', index_col=0)
features_file = pd.read_csv('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/STR_features.csv', index_col=0)

#Features from our data
#features_file = pd.read_csv('./data/Our_LTR.csv', index_col=0)
#features_file = pd.read_csv('./data/Our_STR.csv', index_col=0)

features_file = features_file.set_index('table_id')

#load the qrels dictionary
with open('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/qrels_dict.pickle', 'rb') as handle:
    qrels = pickle.load(handle)

regression_model = RandomForestRegressor(n_estimators=1000, max_leaf_nodes=4)

#get a list from 1 to 60 which will be split up for k fold cross validation
queries = features_file['query_id'].drop_duplicates()
queries = queries.tolist()

# First count the number of relevant tables in corpus for each query.
num_of_relevant_tables = {}
for query_index, query_string in enumerate(queries):
    qrels_one_query = qrels[query_index + 1]
    num_of_relevant_tables[query_string] = 0
    for t in qrels_one_query:
        if(qrels_one_query[t] > 0):
            num_of_relevant_tables[query_string] += 1

kf = KFold(n_splits=5, random_state=2, shuffle=True)

total_ndcg_5, total_ndcg_10, total_ndcg_15, total_ndcg_20, \
    total_prec_25, total_prec_50, total_prec_75, total_prec_100, \
    total_rec_25, total_rec_50, total_rec_75, total_rec_100 = \
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

for train_index, test_index in kf.split(queries):
    #get the features for the rows that match the query and fit the model
    X = features_file.loc[features_file['query_id'].isin(train_index)]
    Y = features_file.loc[features_file['query_id'].isin(train_index)]
    X = X.drop(labels='rel', axis = 1)
    Y = Y['rel']
    regression_model.fit(X.iloc[:, 1:], Y)

    #in this loop I evaluate the ndcg score for every query in the validation dataset
    for query_id in test_index:

        # Holds the number of relevant tables retrieved until i'th position.
        num_relevant_tables_retrieved = [0]
        num_results = 0  # Will count number of results that have annotation.
        predicted_relevance, actual_relevance = [], []

        query_id_actual = query_id + 1
        tables_one_query = features_file.loc[features_file['query_id'] == query_id_actual]
        tables_one_query = tables_one_query.drop(labels=['query_id', 'rel'], axis = 1)

        results = regression_model.predict(tables_one_query)
        table_id_and_rankings = pd.DataFrame([tables_one_query.index, results]).T
        table_id_and_rankings.columns = ['table_id', 'ranking']
        table_id_and_rankings = table_id_and_rankings.sort_values(by=['ranking'], axis=0, ascending=False)
        qrels_one_query = qrels[query_id_actual]


        for index, row in table_id_and_rankings.iterrows():
            if(row['table_id'] in qrels_one_query):
                num_results += 1
                actual_relevance.append(qrels_one_query[row['table_id']])
                predicted_relevance.append(row['ranking'])
                last_num_of_relevant_tables = num_relevant_tables_retrieved[
                    len(num_relevant_tables_retrieved) - 1]
                # If table was indeed relevant, increment with 1.
                if (qrels_one_query[row['table_id']] > 0):
                    num_relevant_tables_retrieved.append(
                        last_num_of_relevant_tables + 1)
                else:
                    num_relevant_tables_retrieved.append(
                        last_num_of_relevant_tables
                    )
        total_ndcg_5 += ndcg_score(
            [actual_relevance], [predicted_relevance], k=5)
        total_ndcg_10 += ndcg_score(
            [actual_relevance], [predicted_relevance], k=10)
        total_ndcg_15 += ndcg_score(
            [actual_relevance], [predicted_relevance], k=15)
        total_ndcg_20 += ndcg_score(
            [actual_relevance], [predicted_relevance], k=20)
        # Calculate number of relevant tables at 4 levels.
        num_relevant_tables_25 = num_relevant_tables_retrieved[int(0.25 * len(num_relevant_tables_retrieved))]
        num_relevant_tables_50 = num_relevant_tables_retrieved[int(0.50 * len(num_relevant_tables_retrieved))]
        num_relevant_tables_75 = num_relevant_tables_retrieved[int(0.75 * len(num_relevant_tables_retrieved))]
        num_relevant_tables_100 = num_relevant_tables_retrieved[len(num_relevant_tables_retrieved) - 1]

        # Calculate precision at 4 levels. See slides first week.
        total_prec_25 += num_relevant_tables_25 / num_results
        total_prec_50 += num_relevant_tables_50 / num_results
        total_prec_75 += num_relevant_tables_75 / num_results
        total_prec_100 += num_relevant_tables_100 / num_results

        # Calculate recall at 4 leve ls. See slides first week.
        num_relevant_in_corpus = num_of_relevant_tables[query_string]
        if num_relevant_in_corpus > 0:
            total_rec_25 += num_relevant_tables_25 / num_relevant_in_corpus
            total_rec_50 += num_relevant_tables_50 / num_relevant_in_corpus
            total_rec_75 += num_relevant_tables_75 / num_relevant_in_corpus
            total_rec_100 += num_relevant_tables_100 / num_relevant_in_corpus

print(total_ndcg_5 / 60, total_ndcg_10 / 60, total_ndcg_15 / 60, total_ndcg_20 / 60, total_prec_25 / 60, total_prec_50 / 60, total_prec_75 / 60, total_prec_100 / 60, total_rec_25 / 60, total_rec_50 / 60, total_rec_75 / 60, total_rec_100 / 60)