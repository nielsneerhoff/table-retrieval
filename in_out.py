import pandas as pd

FEATURES_FILE = './feature/features.csv'
QUERIES_FILE = './data/queries.csv'

class InOut:

    @staticmethod
    def read_features(features_file = FEATURES_FILE):
        data = pd.read_csv(features_file)
        return data

    @staticmethod
    def write_csv(csv_file):
        return pd.write_csv(csv_file)

    @staticmethod
    def read_queries(queries_file = QUERIES_FILE):
        data = pd.read_csv(queries_file)
        return data