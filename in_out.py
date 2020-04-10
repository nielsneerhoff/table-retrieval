import pandas as pd
import json

FEATURES_FILE = './feature/features.csv'
QUERIES_FILE = './data/queries.csv'
TABLES_FILE = './data/relevant_Tables_working.json'
QRELS_FILE = './data/qrels.txt'

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

    @staticmethod
    def read_tables(tables_file=TABLES_FILE):
        with open(tables_file, 'r') as f:
            data = json.load(f)
        return data

    @staticmethod
    def read_qrels(qrels_file=QRELS_FILE):
        data = pd.read_csv(qrels_file, sep='\t', names=['query', 'nothing', 'table_id', 'relevance'])
        return data

    @staticmethod
    def read_tables_list(tables_list_file):
        with open(tables_list_file, 'r') as file_reader:
            for table in file_reader:
                table = json.loads(table)
