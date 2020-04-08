from whoosh.fields import TEXT, NUMERIC, Schema
from whoosh.index import open_dir
from re import sub

# TODO
# QUESTIONS TO DISCUSS (IN REPORT)
# 1. Do we want to keep doubles or stick with unique values?
# 2. Do we want to remove hyperlinks?
# 3. Do we want to lemmatize/stem? (Seems logical to do)
# 4. Why do we get better NDCG results without cleaning?

# Example cleaned field:
# Denotes players who are currently on the Bobcats roster Denotes players who are currently on the Bobcats roster Denotes players who are currently on the Bobcats roster Denotes players who are currently on the Bobcats roster Denotes players who are currently on the Bobcats roster No No Jersey number Jersey number Pos Position Position G Basketball positions Basketball positions F Basketball positions C Basketball positions Pts Point basketball Point basketball Reb Rebound basketball Ast Assist basketball

SCHEMA = Schema(
    id = TEXT(stored=True),
    headers = TEXT(stored=True),
    numCols = NUMERIC(stored=True),
    page_title = TEXT(stored=True),
    numDataRows = NUMERIC(stored=True),
    section_title = TEXT(stored=True),
    numHeaderRows = NUMERIC(stored=True),
    caption = TEXT(stored=True),
    body = TEXT(stored=True),
    titles = TEXT(stored=True),
    caption_and_headers = TEXT(stored=True),
    all_concatenated = TEXT(stored = True))

def to_fields(identifier, table):
    fields = {}

    # Text values.
    fields['headers'] = clean_list(table['title'])
    fields['page_title'] = clean_string(table['pgTitle'])
    fields['section_title'] = clean_string(table['secondTitle'])
    fields['caption'] = clean_string(table['caption'])
    fields['body'] = clean_matrix(table['data'])
    fields['titles'] = fields['page_title'] + ' ' + fields['section_title']
    fields['caption_and_headers'] = fields['caption'] + ' ' + fields['headers']
    fields['all_concatenated'] = fields['titles'] + fields['caption_and_headers'] + fields['body']
    
    # Numeric values.
    fields['id'] = identifier
    fields['numDataRows'] = int(table['numDataRows'])
    fields['numCols'] = int(table['numCols'])
    fields['numHeaderRows'] = int(table['numHeaderRows'])

    return fields

def clean_string(string):
    """ Cleans a string from special characters, numbers and hyperlinks. """
    if string:
        string = sub('[^A-Za-z0-9]+', ' ', string.split('|', 1)[0])
    return string.strip()

def clean_list(array):
    """ Returns a string with concatenated cleaned strings of entire array. """
    string = ''
    for i in range(len(array) - 1):
        string += clean_string(array[i])
        if string:
            string += ' '
    if len(array) - 1 > -1:
        string += clean_string(array[len(array) - 1])
    return string

def clean_matrix(matrix):
    """ Returns a string with concatenated cleaned strings of entire matrix. """
    string = ''
    for i in range(len(matrix) - 1):
        row = matrix[i]
        string += clean_list(row)
        if string:
            string += ' '
    if len(matrix) - 1 > -1:
        string += clean_list(matrix[len(matrix) - 1])
    return string
