from nltk.corpus import wordnet

def get_synsets(token):
    return wordnet.synsets(token)

def get_hypernyms(token):
    synsets = get_synsets(token)
    hypernyms = []
    for ss in synsets:
        for hypernym in ss.hypernyms():
            # Parse the token of this hypernym, replace '_' by ' '.
            hypernym = hypernym._name.split('.')[0].replace('_', ' ')
            hypernyms.append(hypernym)
    print(hypernyms)

# get_hypernyms('interest')

from gensim.models import Word2Vec
print('--------LOAD WIKI2VEC MODEL--------')
model = Word2Vec.load("data/en_1000_no_stem/en.model")
print('---------------DONE----------------')