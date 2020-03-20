import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score, confusion_matrix
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_selection import mutual_info_classif
from sklearn.model_selection import KFold
from statistics import mean
from sklearn.metrics import confusion_matrix
from sklearn.feature_selection import SelectKBest, f_classif
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification



from sklearn.ensemble import Ran

#todo
#get cross validation function using stratified crossval
#implement feature selection to get best features


#workflow is the following
#preprocess dataframe
#remove features if you want k best features
#select classifier
#Train classifier
#Test and eval classifier



def get_classifier(name):
    if name == 'Tree':
        classifier = tree.DecisionTreeClassifier()
    if name == 'Forest':
        classifier = RandomForestClassifier(n_estimators=100)
    if name == 'AdaBoost':
        classifier = AdaBoostClassifier(n_estimators=30)
    if name == 'XGB':
        classifier =  xgb.XGBClassifier()
        # classifier = xgb.XGBClassifier(silent=False,
        #               scale_pos_weight=1,
        #               learning_rate=0.01,
        #               colsample_bytree = 0.4,
        #               subsample = 0.8,
        #               objective='binary:logistic',
        #               n_estimators=1000,
        #               reg_alpha = 0.3,
        #               max_depth=4,
        #               gamma=10)
    if name == 'SVM':
        classifier = svm.SVC()
    if name == 'KNN':
        classifier = KNeighborsClassifier(n_neighbors=10)
    if name == 'Naive':
        classifier = GaussianNB()
    return classifier

def train_classifier(classifier, training_dataframe, training_features_series):
    if classifier is not None:
        classifier.fit(training_dataframe, training_features_series)

def performance_classifier(test_predictions, test_targets):
    auc_score = roc_auc_score(test_targets, test_predictions)
    precision = precision_score(test_targets, test_predictions)
    recall = recall_score(test_targets, test_predictions)
    accuracy = accuracy_score(test_targets, test_predictions)
    confusion = confusion_matrix(test_targets, test_predictions)
    return auc_score, precision, recall, accuracy, confusion


def test_eval_classifier(classifier, test_dataframe, test_targets):
    if classifier is not None:
        test_predictions = classifier.predict(test_dataframe)
        return performance_classifier(test_predictions, test_targets)

def k_fold_evaluation(classifier, full_dataframe, k):
    AUC = list()
    PRECISION = list()
    RECAL = list()
    ACCURACY = list()
    AUC_Train = list()
    PRECISION_Train = list()
    RECAL_Train = list()
    ACCURACY_Train = list()
    kf = KFold(n_splits=k, shuffle=True, random_state=2)
    for train_index, test_index in kf.split(full_dataframe):
        train = full_dataframe.iloc[train_index]
        test = full_dataframe.iloc[test_index]
        training_labels = train['truth_class']
        training_features = train.drop(columns=['truth_class'])
        testing_labels = test['truth_class']
        testing_features = test.drop(columns=['truth_class'])
        train_classifier(classifier, training_features, training_labels)
        auc, precision, recall, accuracy, confusion = test_eval_classifier(classifier, testing_features, testing_labels)
        auc_T, precision_T, recall_T, accuracy_T, confusion_T = test_eval_classifier(classifier, training_features, training_labels)
        AUC_Train.append(auc_T)
        PRECISION_Train.append(precision_T)
        RECAL_Train.append(recall_T)
        ACCURACY_Train.append(accuracy_T)
        AUC.append(auc)
        PRECISION.append(precision)
        RECAL.append(recall)
        ACCURACY.append(accuracy)
    return mean(AUC), mean(PRECISION), mean(RECAL), mean(ACCURACY), confusion, mean(AUC_Train), mean(PRECISION_Train), mean(RECAL_Train), mean(ACCURACY_Train), confusion_T

def gain_info(training_dataframe, training_features_series):
    info_gain = mutual_info_classif(training_dataframe, training_features_series)
    result = dict(zip(training_dataframe.columns,info_gain))
    gn = pd.Series(result).to_frame()
    gn = gn.reset_index()
    gn.columns = ['features', 'information']
    gn = gn.sort_values(ascending=False, by=['information'])
    return gn


def preprocess_dataframe(dataframe, rule):
    if rule == 'zero':
        dataframe = dataframe.fillna(0)
    if rule == 'mean':
        dataframe = dataframe.fillna(dataframe.mean())
    return dataframe

def k_best_features(k, full_dataframe):
    Y = full_dataframe['truth_class']
    X = full_dataframe.drop(columns=['truth_class'])
    k_best = SelectKBest(score_func=f_classif, k=k)
    k_best_features = k_best.fit_transform(X, Y)
    k_best_names = [X.columns[k] for k in k_best.get_support(indices=True)]
    # print(k_best_names)
    new_train = pd.DataFrame(k_best_features)
    new_train.columns = k_best_names
    new_train['truth_class'] = Y
    return new_train


def print_confusion_matrix(confusion_matrix, class_names, figsize=(10, 7), fontsize=14):
    """Prints a confusion matrix, as returned by sklearn.metrics.confusion_matrix, as a heatmap.

    Arguments
    ---------
    confusion_matrix: numpy.ndarray
        The numpy.ndarray object returned from a call to sklearn.metrics.confusion_matrix. 
        Similarly constructed ndarrays can also be used.
    class_names: list
        An ordered list of class names, in the order they index the given confusion matrix.
    figsize: tuple
        A 2-long tuple, the first value determining the horizontal size of the ouputted figure,
        the second determining the vertical size. Defaults to (10,7).
    fontsize: int
        Font size for axes labels. Defaults to 14.

    Returns
    -------
    matplotlib.figure.Figure
        The resulting confusion matrix figure
    """
    df_cm = pd.DataFrame(
        confusion_matrix, index=class_names, columns=class_names,
    )
    fig = plt.figure(figsize=figsize)
    try:
        heatmap = sns.heatmap(df_cm, annot=True, fmt="d")
    except ValueError:
        raise ValueError("Confusion matrix values must be integers.")
    heatmap.yaxis.set_ticklabels(heatmap.yaxis.get_ticklabels(), rotation=0, ha='right', fontsize=fontsize)
    heatmap.xaxis.set_ticklabels(heatmap.xaxis.get_ticklabels(), rotation=45, ha='right', fontsize=fontsize)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    return fig

# def select_k_best_classifier(k):
#
#
#
#     X_new = SelectKBest(score_func=f_classif, k=5)
#     X_new.fit_transform(train, train_labels)
#
#
#
#
