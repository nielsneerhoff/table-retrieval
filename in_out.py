import pandas as pd
import json
import urllib

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

    @staticmethod
    def write_csv(dataframe, path):
        dataframe.to_csv(path)

    @staticmethod
    def read_csv(path):
        return pd.read_csv(path)

    @staticmethod
    def read_json(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
            f.close()
        except FileNotFoundError:
            return None

    @staticmethod
    def write_json(data, path):
        with open(path, 'w') as f:
            f.write(json.dumps(data, indent=4))
        f.close()


    @staticmethod
    def download_rdf2vec(url, path):
        rdf2vec = {}
        f = urllib.request.urlopen(url)
        entity_name = ''
        for coded_line in f:
            line = coded_line.decode("utf-8")
            try:
                preprocessed = line.split('http://dbpedia.org/resource/')[1].split('>')
                vector = preprocessed[1].strip()
            
                if preprocessed[0].find('Category:') != -1:
                    category_name = preprocessed[0].split('Category:')[1]
                    rdf2vec[entity_name]['categories'].append(category_name.lower())
                    # rdf2vec[entity_name]['categories'][category_name.lower()] = { 'vector' : list(map(lambda x: float(x), vector.split(' '))) }
                else:
                    entity_name = preprocessed[0].strip().lower()
                    rdf2vec[entity_name] = { 'vector' : list(map(lambda x: float(x), vector.split(' '))) }
                    rdf2vec[entity_name]['categories'] = []
                    print(entity_name)
            except:
                pass
        InOut.write_json(rdf2vec, path)
        return rdf2vec
        