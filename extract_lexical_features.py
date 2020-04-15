import wikipediaapi
import wikipedia
import pageviewapi
from extract_semantic_features import *
from nltk.tokenize import word_tokenize
import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen

wiki = wikipediaapi.Wikipedia()

HEADERS = ['query_id', 'query', 'table_id', 'row', 'col', 'nul', 'in_link', 'out_link', 'pgcount', 'tImp',
            'tPF', 'leftColhits', 'SecColhits', 'bodyhits', 'PMI', 'qInPgTitle', 'qInTableTitle', 'yRank',
            'csr_score', 'idf1', 'idf2', 'idf3', 'idf4', 'idf5', 'idf6', 'max', 'sum', 'avg', 'sim', 'emax',
            'esum', 'eavg', 'esim', 'cmax', 'csum', 'cavg', 'csim', 'remax', 'resum', 'reavg', ' resim',
            'query_l', 'rel']

def extract_lexical_features(query, table):
    """ Main function for extracting all lexical features
    """
    page = find_page_table(table)
    
    lexical_features = {
        'nul' : nul(table),
        'in_links' : in_links(page),
        'out_links' : out_links(page),
        'pgcount' : pageViews(page),
        'tImp' : tableImportance(page),
        'leftColhits' : hitsLC(query, table),
        'SecColhits' : hitsSLC(query, table),
        'bodyhits' : hitsB(query, table),
        'qInPgTitle' : qInPgTitle(query, table),
        'qInTableTitle' : qInTableTitle(query, table),
        'query_l' : query_l(query)
    }

    return lexical_features


def find_page_table(table):
    """Retrieves the page corresponding to the table
    
    :param table: table object
    :return: Returns the wikipedia page object
    """    
    page_title = wikipedia.search(table['pgTitle'])[0]
    return wiki.page(page_title)

def nul(table):
    """Retrieves number of null valued cells from table
    
    :param table: table object
    :return: number of cells that are empty
    """    
    count = 0
    for row in table['data']:
        for cell in row:
            if cell == '':
                count += 1
    return count

def in_links(page):
    """Retrieves the number of inlinks from the table
    
    :param page: Wikipedia page
    :return: in links of page
    """    
    return len(list(page.backlinks.keys()))

def out_links(page):
    """ Retrieves the number of outlinks from the table
    """
    return len(list(page.links.keys()))

def pageViews(page):
    """ Retrieves the number of page views for the table page in the period 01-01-2020 - 01-04-2020.
    :param page:
    :return:
    """
    start_date = '20200101'  
    end_date = '20200401'   
    n_of_page_views = 0
    try:
        page_views = pageviewapi.per_article('en.wikipedia', page.title, start_date, end_date,
                                         access='all-access', agent='all-agents', granularity='daily')
        for article in page_views['items']:
            n_of_page_views += article['views']
    except:
        n_of_page_views = 0

    return n_of_page_views / (31 + 29 + 31)

def tableImportance(page):
    """ Inverse of the number of tables on the wikipedia page
    """
    try:
        with urlopen(page.fullurl) as response:
            soup = BeautifulSoup(response, 'html.parser')
            return 1 / len(soup.find_all('table', {"class": "wikitable"}))
    except:
        return 0


def hitsLC(query, table):
    """ Number of hits in leftmost column
    """
    count = 0
    words_query = query.split()
    for row in table['data']:
        if row[0].split() in words_query:
            count += 1
    return count

def hitsSLC(query, table):
    """ Number of hits in second to leftmost column
    """
    count = 0
    words_query = query.split()
    for row in table['data']:
        if len(row) > 1:
            if row[1].split() in words_query:
                count += 1
    return count

def hitsB(query, table):
    """ Number of hits in the table body
    """
    count = 0
    words_query = query.split()
    for row in table['data']:
        for cell in row:
            if cell.split() in words_query:
                count += 1
    return count

def qInPgTitle(query, table):
    """ Number of query tokens found in the page title divided by the total number of tokens
    """
    tokens_query = set(word_tokenize(query))
    tokens_page_title = set(word_tokenize(table['pgTitle']))
    table_string = table['caption'] + ' ' + table['secondTitle'] + ' ' + table['pgTitle']
    for header in table['title']:
        table_string += ' ' + header
    for row in table['data']:
        for cell in row:
            table_string += ' ' + cell
            
    no_found_in_page_title = len(tokens_query.intersection(tokens_page_title))
    no_found_in_page = len(set(word_tokenize(table_string)))

    return no_found_in_page_title / no_found_in_page



def qInTableTitle(query, table):
    """ Number of query tokens found in the table title divided by the total number of tokens
    """
    tokens_query = set(word_tokenize(query))
    table_string = ''
    for header in table['title']:
        table_string +=  header + ' '
    tokens_table_title = set(word_tokenize(table_string))
    table_string += table['caption'] + ' ' + table['secondTitle'] + ' ' + table['pgTitle']
    for row in table['data']:
        for cell in row:
            table_string += ' ' + cell
            
    no_found_in_table_title = len(tokens_query.intersection(tokens_table_title))
    no_found_in_page = len(set(word_tokenize(table_string)))

    return no_found_in_table_title / no_found_in_page

def query_l(query):
    """returns the length of the query
    
    :param query: Query
    :return: length of query
    """    
    return len(query.split())        