from in_out import InOut
from feature_set import *
from time import time

features = InOut.read_features()
wiki_tables_features = subset_features(features, 'wiki')
web_tables_features = subset_features(features, 'web')
ltr_features = subset_features(features, 'ltr')
str_features = subset_features(features, 'str')



queries = InOut.read_queries()

tables = InOut.read_tables()

qrels = InOut.read_qrels()

large_tables_file = './data/tables.jsonl'

features_queries = extract_features(queries, tables, qrels, large_tables_file)
