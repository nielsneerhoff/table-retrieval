from gensim.models import Word2Vec
import pandas as pd
import pickle

print('--------LOAD WIKI2VEC MODEL--------')
model = Word2Vec.load("C:/Users/wybek/Downloads/en_1000_no_stem/en.model")
print('---------------DONE----------------')



queries = pd.read_csv('./data/queries.csv')
queries = queries['query'].tolist()
queries = [item.strip() for item in queries]

similar_terms = {}

word_vectors = model.wv

for i in queries:
    for j in i.split(" "):
        word = str(j)
        if word in word_vectors:
            expansions = model.wv.most_similar(positive=word, topn=10)
            word_list = list()
            for n in expansions:
                word_list.append(n[0])
            similar_terms[word] = word_list
print(similar_terms)
with open('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/query_expansion.pickle', 'wb') as handle:
    pickle.dump(similar_terms, handle, protocol=pickle.HIGHEST_PROTOCOL)