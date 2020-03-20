from in_out import InOut
from feature_set import extract_features

io = InOut()
features = io.read_features()
wiki_tables_features = extract_features(features, 'wiki')
web_tables_features = extract_features(features, 'web')
ltr_features = extract_features(features, 'ltr')
str_features = extract_features(features, 'str')