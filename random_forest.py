import pandas as pd
import sklearn.model_selection
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error
from statistics import mean


from sklearn import ensemble

X = pd.read_csv('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/feature/features.csv')
y = X['rel']
X = X.drop(['query_id', 'query', 'table_id', 'rel'], axis=1)


#forest = RandomForestRegressor(n_estimators=1000, max_depth=

fold = KFold(n_splits=5, shuffle=True, random_state=3)

MAE_Training = list()
MAE_Validation = list()

for train_index, test_index in fold.split(X):
    #model = Lasso(alpha=0.001, max_iter=900000)
    model = RandomForestRegressor(n_estimators=1000, max_depth=3)

    print('new fold')
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y[train_index], y[test_index]
    model.fit(X_train, y_train)
    train_predictions = model.predict(X_train)
    validation_predictions = model.predict(X_test)
    print('training error ' + str(mean_absolute_error(y_train, train_predictions)))
    print('validation error ' + str(mean_absolute_error(y_test, validation_predictions)))
    MAE_Training.append(mean_absolute_error(y_train, train_predictions))
    MAE_Validation.append(mean_absolute_error(y_test, validation_predictions))
    # for pred, actual in zip(validation_predictions, y_test):
    #     print(str(pred) + " " + str(actual))

print("Average MAE 5 folds training: " + str(mean(MAE_Training)))
print("Average MAE 5 folds validation: " + str(mean(MAE_Validation)))


