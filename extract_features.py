import pandas as pd
import json
import numpy as np
import gensim
from extract_semantic_features import *
from extract_semantic_dictionaries import *
from in_out import InOut as IO

HEADERS = ['query_id', 'query', 'table_id', 'row', 'col', 'nul', 'in_link', 'out_link', 'pgcount', 'tImp',
            'tPF', 'leftColhits', 'SecColhits', 'bodyhits', 'PMI', 'qInPgTitle', 'qInTableTitle', 'yRank',
            'csr_score', 'idf1', 'idf2', 'idf3', 'idf4', 'idf5', 'idf6', 'max', 'sum', 'avg', 'sim', 'emax',
            'esum', 'eavg', 'esim', 'cmax', 'csum', 'cavg', 'csim', 'remax', 'resum', 'reavg', ' resim',
            'query_l', 'rel']

base_path_dicts = './data/dictionaries/'

def extract_features(queries, tables, qrels):
    """ Extract features based on the queries and tables
    :param queries: pandas dataframe of queries of the form query_id, query
    :param tables: json of tables
    :param qrels: pandas dataframe of queries of the form query_id, 0, table_id, score

            return new queries dataframe with following features added

            Query features
            QLEN:               Number of query items                                           {1, ..., n}
            IDF_f:              Sum of query IDF scores in field f                              [0, ∞)
            
            Table features
            #rows:              The number of rows in the table                                 {1, ..., n}
            #cols:              The number of columns in the table                              {1, ..., n}
            #of NULLs in table  The number of empty table cells                                 {0, ..., n}
            PMI                 The ACSDb-based schema coherency score                          (−∞, ∞)
            inLinks             Number of in-links to the page embedding the table              {1, ..., n}
            outLinks            Number of out-links from the page embedding the table           {1, ..., n}
            pageViews           Number of page views                                            {1, ..., n}
            tableImportance     Inverse of number of tables on the page                         (0, 1]
            tablePageFraction   Ratio of table size to page size                                (0, 1]

            Query + Table features
            #hitsLC             Total query term frequency in the leftmost column cells         {1, ..., n}
            #hitsSLC            Total query term frequency in second-to-leftmost column cells   {1, ..., n}
            #hitsB              Total query term frequency in the table body                    {1, ..., n}
            qInPgTitle          Ratio of the number of query tokens found in 
                                        page title to total number of tokens                    [0, 1]
            qInTableTitle       Ratio of the number of query tokens found in 
                                        table title to total number of tokens                   [0, 1]
            yRank               Rank of the table’s Wikipedia page in Web search 
                                        engine results for the query                            {1, ..., n}
            MLM similarity      Language modeling score between query and multi-field 
                                        document repr. of the table                             (−∞, 0)

            Semantic features

    """


    # Main Dictionary of features
    features = IO.read_json(base_path_dicts + 'current_features.json')
    if features == None:
        features = {}


    # Dictionary of the queries
    queries_dict = IO.read_json(base_path_dicts + 'queries.json')
    if queries_dict == None:
        queries_dict = {}
        for row in queries.itertuples():
            queries_dict[row.query_id] = row.query.strip()
        IO.write_json(queries_dict, base_path_dicts + 'queries.json')

    tables_dict = IO.read_json(base_path_dicts + 'tables.json')
    if tables_dict == None:
        tables_dict = tables
        IO.write_json(tables_dict, base_path_dicts + 'tables.json')

    all_words = None
    all_entities = None
    dataframe = []

    print('---------- LOADING DOCUMENT TO WORDS MODEL ----------')
    query_to_words = IO.read_json(base_path_dicts + 'query_to_words.json')
    table_to_words = IO.read_json(base_path_dicts + 'table_to_words.json')
    if query_to_words == None or table_to_words == None:
        all_words, query_to_words, table_to_words = get_all_words(queries_dict, tables_dict)
    print('---------- DONE LOADING DOCUMENT TO WORDS MODEL ----------\n')
    

    print('---------- LOADING WORD2VEC MODEL ----------')
    word2vec_model = IO.read_json(base_path_dicts + 'word2vec.json')
    if word2vec_model == None:
        word2vec_model = gensim.models.KeyedVectors.load_word2vec_format('./data/GoogleNews-vectors-negative300.bin', binary=True)
        if all_words == None:
            all_words = get_all_words_from_json(query_to_words, table_to_words)
        word2vec_model = create_word2vec_model(word2vec_model, all_words)
    print('---------- DONE LOADING WORD2VEC MODEL ----------\n')


    print('---------- LOADING DOCUMENT TO ENTITIES MODEL ----------')
    query_to_entities = IO.read_json(base_path_dicts + 'query_to_entities.json')
    table_to_entities = IO.read_json(base_path_dicts + 'table_to_entities.json')
    if query_to_entities == None or table_to_entities == None:
        all_entities, query_to_entities, table_to_entities = get_all_entities(queries_dict, tables_dict)
    print('---------- DONE LOADING DOCUMENT TO ENTITIES MODEL ----------\n')


    print('---------- LOADING RDF2VEC SUBSET MODEL ----------')
    rdf2vec_model = IO.read_json(base_path_dicts + 'rdf2vec.json')
    if rdf2vec_model == None:
        rdf2vec_model = IO.read_json(base_path_dicts + 'rdf2vec_large.json')
        if rdf2vec_model == None:
            url = "http://data.dws.informatik.uni-mannheim.de/rdf2vec/models/DBpedia/2016-04/GlobalVectors/1_uniform/DBpediaVecotrs200_20Shuffle.txt"
            rdf2vec_model = IO.download_rdf2vec(url, base_path_dicts + 'rdf2vec_large.json')
        if all_entities == None:
            all_entities = get_all_entities_from_json(query_to_entities, table_to_entities)
        rdf2vec_model = create_rdf2vec_model(rdf2vec_model, all_entities)
    print('---------- DONE LOADING RDF2VEC MODEL ----------\n')

    
    for row in qrels.itertuples():

        q_id = str(row.query)
        t_id = str(row.table_id)
        rowid = q_id + '_###_' + t_id

        table = tables_dict[row.table_id]
        query = queries_dict[q_id]

        if rowid not in features.keys():
            features[rowid] = {
                'query_id' : q_id,
                'query' : query,
                'table_id' : t_id,
                'row' : table['numDataRows'],
                'col' : table['numCols']
            }
            
        if 'esim' not in features[rowid].keys():
            features[rowid]['esim'] = extract_semantic_features(query_to_words[q_id], table_to_words[t_id], word2vec_model)
        if 'eavg' not in features[rowid].keys():
            features[rowid]['eavg'], features[rowid]['emax'], features[rowid]['esum'] = \
                extract_semantic_features(query_to_words[q_id], table_to_words[t_id], word2vec_model, False)

        if 'resim' not in features[rowid].keys():
            features[rowid]['resim'] = extract_semantic_features(query_to_entities[q_id], table_to_entities[t_id], rdf2vec_model, True, False)
        if 'reavg' not in features[rowid].keys():
            features[rowid]['reavg'], features[rowid]['remax'], features[rowid]['resum'] = \
                extract_semantic_features(query_to_entities[q_id], table_to_entities[t_id], rdf2vec_model, False, False)

        dataframe.append(features[rowid])
    
    IO.write_json(features, base_path_dicts + 'current_features.json')
    IO.write_csv(dataframe, base_path_dicts + 'features.csv')
    return pd.DataFrame(dataframe)
