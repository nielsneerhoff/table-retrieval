import pandas as pd
import re
import json
import requests


def retrieve_table_features(table, tables_list_file):
    table['nul'] = 0
    table['in_link'] = 0
    table['out_link'] = 0
    table['pgcount'] = 0     # pageviews
    table['tImp'] = 0        # table importance - Inverse of number of tables on the page
    table['tPF'] = 0         # table page fraction - Ratio of table size to page size
    table['PMI'] = 0         # The ACSDb-based schema coherency score
    for row_table in table['data']:
        for row_table_cell in row_table:
            if row_table_cell == None or row_table_cell == '':
                table['nul'] += 1
            table['out_link'] += len(re.compile( r'(\[.*?\|.*?\])').findall(row_table_cell))
    
def get_entities_api(text):
    """ Retrieve list entities from text using the DBpedia API
    returns list of entities
    """
    # text = 'United States World Sghoccer'
    entities = []
    param = { 'text' : text }
    url='http://api.dbpedia-spotlight.org/en/candidates'
    r = requests.get(url = url, params=param) 
    if r.status_code != 200:
        raise ConnectionError
        return print('Error API')
    content = json.loads(r.content)
    if 'surfaceForm' in content['annotation'].keys():
        if isinstance(content['annotation']['surfaceForm'], list):
            entities = [name['@name'] for name in content['annotation']['surfaceForm']]
        else:
            entities = [content['annotation']['surfaceForm']['@name']]
    return entities

def get_entities_regex(text):
    """ Retrieve list of entities from text using Regex
    returns list of entities
    """
    entities = re.compile( r'(\|.*?\])').findall(text)
    for index, string in enumerate(entities):
        entities[index] = string.strip('|]')
    return entities

def set_representation(content, representation='words'):
    """ The “raw” content of a query/table is represented as a set of terms, 
    where terms can be either words or entities.
    :param representation: 'words' or 'entities'
    """
    content_set = set()

    if representation == 'words':
        if isinstance(content, str):
            content_set = set(content.split())
        else:
            headers = [t.split() for t in content.title]
            content_set = set([headers, content.caption.split(), content.pgTitle.split()])

    if representation == 'entities':
        if isinstance(content, str):
            content_set = set(get_entities_api(content))
        else:
            test= get_entities_api(content)
            entities_in_col = [0 for i in range(content['numCols'])]
            for j in range(content['numCols']):
                for i in range(content['numDataRows']):
                    test = get_entities_regex(content['data'][i][j])
                    entities_in_col[i] += len(get_entities_regex(content['data'][i][j]))
            string = content.caption + ' ' + content.pgTitle
            for header in content.title:
                string += ' ' + header
            content_set = set(get_entities_regex(string))

    return content_set
    


def extract_features(queries, tables, qrels, tables_list_file):
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
    dataframe = []
    queries_dict = {}

    table_features = {}

    for row in queries.itertuples():
        queries_dict[row.query_id] = row.query.strip()
    
    for row in qrels.itertuples():
        query_id = row.query
        query = queries_dict[query_id]
        table_id = row.table_id
        table = tables[table_id]

        set_representation(table, 're')

        # row = table['numDataRows']
        # col = table['numCols']

        # if 'nul' not in table:
            # retrieve_table_features(table, tables_list_file)
        # nul = table['nul']
        # in_link
        # out_link = table['out_link']
        # pgcount = table['pgcount']
        # tImp = table['tImp']
        # tPF = table['tPF']
    
        dataframe.append({
            'query_id' : query_id,
            'query' : query,
            'table_id' : table_id,
        #     'row' : row,
        #     'col' : col,
        #     'nul' : nul,
        #     'in_link',
        #     'out_link' : out_link,
        #     'pgcount',
        #     'tImp',
        #     'tPF',
        #     'leftColhits',
        #     'SecColhits',
        #     'bodyhits',
        #     'PMI',
        #     'qInPgTitle',
        #     'qInTableTitle',
        #     'yRank',
        #     'csr_score',
        #     'idf1',
        #     'idf2',
        #     'idf3',
        #     'idf4',
        #     'idf5',
        #     'idf6',
        #     'max',
        #     'sum',
        #     'avg',
        #     'sim',
        #     'emax',
        #     'esum',
        #     'eavg',
        #     'esim',
        #     'cmax',
        #     'csum',
        #     'cavg',
        #     'csim',
        #     'remax',
        #     'resum',
        #     'reavg',
        #     'resim',
        #     'query_l'
        #     'rel'
        })

    return pd.DataFrame(dataframe)