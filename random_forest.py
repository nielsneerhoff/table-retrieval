import pandas as pd
import sklearn.model_selection
from sklearn.linear_model import Lasso
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
from statistics import mean


from sklearn import ensemble

X = pd.read_csv('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/feature/features.csv')
y = X['rel']
X = X.drop(['query_id', 'query', 'table_id', 'rel'], axis=1)


#forest = RandomForestRegressor(n_estimators=1000, max_depth=

fold = KFold(n_splits=5, shuffle=True, random_state=3)

MSE_Training = list()
MSE_Validation = list()

index = 0
for train_index, test_index in fold.split(X):
    model = Lasso(alpha=0.001, max_iter=500000)

    print('new fold')
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y[train_index], y[test_index]
    model.fit(X_train, y_train)
    train_predictions = model.predict(X_train)
    validation_predictions = model.predict(X_test)
    print('training error ' + str(mean_squared_error(y_train, train_predictions)))
    print('validation error ' + str(mean_squared_error(y_test, validation_predictions)))
    MSE_Training.append(mean_squared_error(y_train, train_predictions))
    MSE_Validation.append(mean_squared_error(y_test, validation_predictions))
    for pred, actual in zip(validation_predictions, y_test):
        print(str(pred) + " " + str(actual))

print("Average MSE 5 folds training: " + str(mean(MSE_Training)))
print("Average MSE 5 folds validation: " + str(mean(MSE_Validation)))


