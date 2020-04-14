from nltk.corpus import wordnet
from gensim.models import Word2Vec

def get_synsets(token):
    return wordnet.synsets(token)

def get_hypernyms(token):
    synsets = get_synsets(token)
    hypernyms = []
    for ss in synsets:
        for hypernym in ss.hypernyms():
            # Hypernym should be a noun.
            if 'noun' in hypernym._lexname:
                # Parse the token of this hypernym, replace '_' by ' '.
                hypernym = hypernym._name.split('.')[0].replace('_', ' ')
                hypernyms.append(hypernym)
    return hypernyms

def get_categories(token):
    pass

def get_hypernym_abstraction(query_string):
    abstraction = ''
    query_terms = query_string.split(' ')
    for term in query_terms:
        hypernyms = get_hypernyms(term)
        abstraction += ' '.join(hypernyms)
    return abstraction

def get_graph_abstraction(query_string):
    abstraction = ''
    query_terms = query_string.split(' ')
    for term in query_terms:
        categories = get_categories(term)
        abstraction += ''.join(categories)
