import pandas as pd
from sklearn.feature_selection import mutual_info_classif



def gain_info(training_dataframe, training_features_series):
    info_gain = mutual_info_classif(training_dataframe, training_features_series)
    result = dict(zip(training_dataframe.columns,info_gain))
    gn = pd.Series(result).to_frame()
    gn = gn.reset_index()
    gn.columns = ['features', 'information']
    gn = gn.sort_values(ascending=False, by=['information'])
    return gn

data = pd.read_csv('./data/Our_STR.csv', index_col=0)
lables = data['rel'].tolist()
data = data.drop(['query_id', 'table_id', 'rel'], axis=1)

print(gain_info(data, lables))