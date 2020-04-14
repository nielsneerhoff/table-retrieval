import wikipediaapi
import wikipedia
from in_out import InOut as IO

from bs4 import BeautifulSoup
from urllib.request import urlopen


# with urlopen('https://en.wikipedia.org/wiki/United_States') as response:
#     soup = BeautifulSoup(response, 'html.parser')
#     print(len(soup.find_all('table', {"class": "wikitable"})))


wiki = wikipediaapi.Wikipedia('en')

query = 'Charlotte Bobcats all-time roster'

page = wikipedia.search(query, 1)[0]

wiki_page = wiki.page(page)

print(wiki_page.fullurl)
print(wiki_page.title)

rdf2vec_model = IO.read_json(base_path_dicts + 'rdf2vec_large.json')

print(len(rdf2vec_model))
