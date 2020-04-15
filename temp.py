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


data = IO.read_json(base_path_dicts + 'current_features.json')

dat = []

for d in data.values():
    dat.append(d)

df = pd.DataFrame(dat)

IO.write_csv(df, base_path_dicts + 'features.csv')

# content = 'world interest rates'

# lemmatizer = WordNetLemmatizer()

# lemmatized_content = ' '.join([lemmatizer.lemmatize(word) for word in content.split()])

# print(lemmatized_content)