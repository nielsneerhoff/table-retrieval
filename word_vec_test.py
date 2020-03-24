import gensim


model = gensim.models.KeyedVectors.load_word2vec_format('C:/Users/wybek/Downloads/GoogleNews-vectors-negative300.bin/GoogleNews-vectors-negative300.bin', binary=True)

print(model['lol'])
print(len(model['lol']))

a = model['I', 'am','query']
print(a)
print(len(a))