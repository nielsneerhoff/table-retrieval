import wikipediaapi
import wikipedia
from in_out import InOut as IO

import pandas as pd

from nltk.stem import WordNetLemmatizer

from bs4 import BeautifulSoup
from urllib.request import urlopen

base_path_dicts = './data/dictionaries/'

# with urlopen('https://en.wikipedia.org/wiki/United_States') as response:
#     soup = BeautifulSoup(response, 'html.parser')
#     print(len(soup.find_all('table', {"class": "wikitable"})))


# wiki = wikipediaapi.Wikipedia('en')

# query = 'Charlotte Bobcats all-time roster'

# page = wikipedia.search(query, 1)[0]

# wiki_page = wiki.page(page)

# print(wiki_page.fullurl)
# print(wiki_page.title)

# rdf2vec_model = IO.read_json(base_path_dicts + 'rdf2vec_large.json')

# print(len(rdf2vec_model))

# from extract_semantic_features import *

# queries = IO.read_json(base_path_dicts + 'queries.json')

rdf2vec_large = {
    'world' : { 'vector' : [0, 0, 0], 'categories' : {'planet' : [1, 1, 1]}},
    'was' : { 'vector' : [0, 0, 0], 'categories' : {'auto' : [2, 2, 2], 'vehicle' : [2, 2, 2]}},
    'interest rate' : { 'vector' : [0, 0, 0], 'categories' : {'planet' : [3, 3, 3]}}
}
entities = ['world', 'interest rate', 'was', 'ads']

cats = [category for entity in entities if entity in rdf2vec_large.keys() for category in rdf2vec_large[entity]['categories'].keys()]
print(cats)
# extended_queries = {}

# entity_vecs = list(map(lambda x: rdf2vec_large[x]['vector'], entities))

# categories = []
# for entity in entities:
#     for key in rdf2vec_large[entity]['categories'].keys():
#         categories.append(key)

# print(entity_vecs)

# category_vecs = list(map(lambda x: rdf2vec_large[x]['categories'].values(), entities))
# category_vecs = [category for entity in entities for category in rdf2vec_large[entity]['categories'].values()]

# entity_vecs += category_vecs

# extended_queries = set(entities) | set(categories)


# print(category_vecs)
# print(entity_vecs)

# dat = []

# for d in data.values():
#     dat.append(d)

# df = pd.DataFrame(dat)

# IO.write_csv(df, base_path_dicts + 'features.csv')

# content = 'world interest rates'

# lemmatizer = WordNetLemmatizer()

# lemmatized_content = ' '.join([lemmatizer.lemmatize(word) for word in content.split()])

# print(lemmatized_content)