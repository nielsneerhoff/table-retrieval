query = set([
    'query_l',
    'idf1',
    'idf2',
    'idf3',
    'idf4',
    'idf5',
    'idf6'
])

wiki = set([
    'row',
    'col',
    'nul',
    'in_link',
    'out_link',
    'pgcount',
    'tImp',
    'tPF',
    'qInPgTitle',
    'qInTableTitle',
    'yRank'
])

web = set([
    'row',
    'col',
    'nul',
    'PMI',
    'leftColHits',
    'SecColhits',
    'bodyhits',
])

LTR = query.union(
    wiki.union(
        web
    )
)

semantics = set([
    'row',
    'col',
    'nul',
    'pmi',
    'hitsLC',
    'hitsSLC',
    'hitsB',
])

STR = LTR.union(semantics)

base = set([
    'query_id',
    'query',
    'query_l',
    'rel'
])

def extract_features(all_features, feature_set_name = None):
    """ Extracts the features corresponding to a feature set name from all features. For instance, passing 'wiki' as feature_set_name returns all columns from all_features corresponding to 'wiki' features. """

    features_names = set()
    if feature_set_name == 'str':
        feature_names  = STR
    elif feature_set_name == 'ltr':
        feature_names = LTR
    elif feature_set_name == 'wiki':
        feature_names = wiki
    elif feature_set_name == 'web':
        feature_names = web
    feature_names = list(feature_names.union(base))
    data = all_features.loc[:, feature_names]
    return data