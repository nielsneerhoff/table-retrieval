import pandas as pd
import numpy as np
import helpfunctions as func
import sklearn.feature_selection
from sklearn.feature_selection import SelectKBest, f_classif

#Todo:
#get k best feature names, create new dataframe

data = pd.read_csv('./feature/features.csv')

#preprocessing
data['Sex'].replace(['female','male'], [0,1],inplace=True)
data = func.preprocess_dataframe(data, 'mean')
data = data.drop(columns=['Name', 'Cabin', 'Embarked', 'Pclass', 'Ticket'])

#Division into train and test
df = pd.DataFrame(np.random.randn(len(data), 2))
msk = np.random.rand(len(df)) < 0.8
train = data[msk]
test = data[~msk]
train_labels = train['Survived']
test_labels = test['Survived']
train = train.drop(columns=['Survived'])
test = test.drop(columns=['Survived'])

#loop over all models
models = ['Tree', 'Forest', 'XGB', 'AdaBoost', 'SVM', 'KNN', 'Naive']
for classifier_type in models:
    #Gets the classifier
    model = func.get_classifier(classifier_type)

    #Info gain
    gain = func.gain_info(train, train_labels)
    print(gain)

    #Trains the classifier
    func.train_classifier(model, train, train_labels)

    #Evaluates classifier on test set
    auc, precision, recall, accuracy = func.test_eval_classifier(model, test, test_labels)

    X_new = SelectKBest(score_func=f_classif, k=2)
    X_new.fit(train, train_labels)
    X_new.fit_transform(train, train_labels)

    # print(X_new.scores_)
    # print(X_new.pvalues_)

    # print("classifier_type: " + classifier_type)
    # print("AUC: " + str(auc))
    # print("Precision: " + str(precision))
    # print("Recall: " + str(recall))
    # print("Accuracy: " +  str(accuracy) + " \n")