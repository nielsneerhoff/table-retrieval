import pandas as pd
import numpy as np
import helperfunctions as func


class Classifier:

    @staticmethod
    def divideData(data, label_name):
        df = pd.DataFrame(np.random.randn(len(data), 2))
        msk = np.random.rand(len(df)) < 0.8
        train = data[msk]
        test = data[~msk]
        train_labels = train[label_name]
        test_labels = test[label_name]
        train = train.drop(columns=[label_name])
        test = test.drop(columns=[label_name])
        return train, train_labels, test, test_labels

    @staticmethod
    def initialize(classifier_type, train, train_labels, test, test_labels):
        model = func.get_classifier(classifier_type)

        gain = func.gain_info(train, train_labels)

        func.train_classifier(model, train, train_labels)

        auc, precision, recall, accuracy = func.test_eval_classifier(model, test, test_labels)

        # print("classifier_type: " + classifier_type)
        # print("AUC: " + str(auc))
        # print("Precision: " + str(precision))
        # print("Recall: " + str(recall))
        # print("Accuracy: " +  str(accuracy) + " \n")

        return None    
        
        









    #     X_new.fit_transform(train, train_labels)

    # print(X_new.scores_)
    # print(X_new.pvalues_)

    # print("classifier_type: " + classifier_type)
    # print("AUC: " + str(auc))
    # print("Precision: " + str(precision))
    # print("Recall: " + str(recall))
    # print("Accuracy: " +  str(accuracy) + " \n")    X_new.fit_transform(train, train_labels)

    # print(X_new.scores_)
    # print(X_new.pvalues_)

    # print("classifier_type: " + classifier_type)
    # print("AUC: " + str(auc))
    # print("Precision: " + str(precision))
    # print("Recall: " + str(recall))
    # print("Accuracy: " +  str(accuracy) + " \n")    X_new.fit_transform(train, train_labels)

    # print(X_new.scores_)
    # print(X_new.pvalues_)

    # print("classifier_type: " + classifier_type)
    # print("AUC: " + str(auc))
    # print("Precision: " + str(precision))
    # print("Recall: " + str(recall))
    # print("Accuracy: " +  str(accuracy) + " \n")    X_new.fit_transform(train, train_labels)

    # print(X_new.scores_)
    # print(X_new.pvalues_)

    # print("classifier_type: " + classifier_type)
    # print("AUC: " + str(auc))
    # print("Precision: " + str(precision))
    # print("Recall: " + str(recall))
    # print("Accuracy: " +  str(accuracy) + " \n")    X_new.fit_transform(train, train_labels)

    # print(X_new.scores_)
    # print(X_new.pvalues_)

    # print("classifier_type: " + classifier_type)
    # print("AUC: " + str(auc))
    # print("Precision: " + str(precision))
    # print("Recall: " + str(recall))
    # print("Accuracy: " +  str(accuracy) + " \n")    X_new.fit_transform(train, train_labels)

    # print(X_new.scores_)
    # print(X_new.pvalues_)

    # print("classifier_type: " + classifier_type)
    # print("AUC: " + str(auc))
    # print("Precision: " + str(precision))
    # print("Recall: " + str(recall))
    # print("Accuracy: " +  str(accuracy) + " \n")    X_new.fit_transform(train, train_labels)

    # print(X_new.scores_)
    # print(X_new.pvalues_)

    # print("classifier_type: " + classifier_type)
    # print("AUC: " + str(auc))
    # print("Precision: " + str(precision))
    # print("Recall: " + str(recall))
    # print("Accuracy: " +  str(accuracy) + " \n")    X_new.fit_transform(train, train_labels)

    # print(X_new.scores_)
    # print(X_new.pvalues_)

    # print("classifier_type: " + classifier_type)
    # print("AUC: " + str(auc))
    # print("Precision: " + str(precision))
    # print("Recall: " + str(recall))
    # print("Accuracy: " +  str(accuracy) + " \n")    X_new.fit_transform(train, train_labels)

    # print(X_new.scores_)
    # print(X_new.pvalues_)

    # print("classifier_type: " + classifier_type)
    # print("AUC: " + str(auc))
    # print("Precision: " + str(precision))
    # print("Recall: " + str(recall))
    # print("Accuracy: " +  str(accuracy) + " \n")    X_new.fit_transform(train, train_labels)

    # print(X_new.scores_)
    # print(X_new.pvalues_)

    # print("classifier_type: " + classifier_type)
    # print("AUC: " + str(auc))
    # print("Precision: " + str(precision))
    # print("Recall: " + str(recall))
    # print("Accuracy: " +  str(accuracy) + " \n")    X_new.fit_transform(train, train_labels)

    # print(X_new.scores_)
    # print(X_new.pvalues_)

    # print("classifier_type: " + classifier_type)
    # print("AUC: " + str(auc))
    # print("Precision: " + str(precision))
    # print("Recall: " + str(recall))
    # print("Accuracy: " +  str(accuracy) + " \n")