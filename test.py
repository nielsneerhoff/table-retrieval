# import re
# string = '[List_of_countries_by_GDP_PPP|GDP (PPP)]1314324134-[3443431sad sd|ad]'

# print(re.findall('(\[.*?\|.*?\])', string))
# for s in re.findall('(\[.*?\|.*?\])', string):
#     string = string.replace(s, s.split('|')[1].split(']')[0])
# print(string)

# st2 = re.findall('(\[.*?\|.*?\])', string)
# print(st2)
# print(string)
# for s in st2:
#     s3 = 3
#     string = string.replace(s, s.split('|')[1].split(']')[0])
#     print(string)
#     print()

# se2 = string.map(lambda x: re.sub(x, x.split('|')[1]), st)

# print(se2)

# se2 = [0] * 8
# query_to_words = {
#     '1' : {'words' : {'et', 'as', 'lf'}},
#     '3' : {'words' : {'as', 'sd'}},
#     '4' : {'words' : {'as', 'er'}}
# }

# sad = {'ear' : {}}
# sad['ear']['asdsa'] = 2
# print(sad)

# print(query_to_words.values())
# for word in ['er', 'et', 'as', 've']:
#     print(len([word for x in query_to_words.values() if word in x['words']]))

# a = {
#     'a',
#     'b',
#     'd'
#     }
# b = {
#     'a' : 1,
#     'b' : 2,
#     'c' : 3
#     }

# s = {'er', 'et', 'as', 've'}

# query = {
#     'words' : list(s),
#     'er' : {
#         'TFIDF' : 2
#     },
#     'et' : {
#         'TFIDF' : 24
#     },
#     'as' : {
#         'TFIDF' : 26
#     },
#     've' : {
#         'TFIDF' : 4
#     }
# }

# query_tfidf = list(map(lambda x: query[x]['TFIDF'], query['words']))
# print(query_tfidf)
# print(list(zip(a,b)))

# print(dict(map(lambda x: x, a)))

# x = set(['e', 'f'])
# y = set(['r', '3'])

# b = {'b' : x}
# z = x.union(set(['r', '3']))

# print(z)

# import numpy as np

# a = [0, 1, 2, 3]

# b = [4, 5, 6, 7]

# c = [8, 9, 10, 11]

# d = [a, b, c]

# e = [c, b, a, a]

# f = [1.5, 1.8, 2.1]

# print(list(zip(list(map(lambda y, z: y * z, d, f)))))

# print(list(map(lambda x: sum(x), zip(list(map(lambda y, z: y * z, d, f))))))

# ret = [0] * len(a)
# for i, col in enumerate(d):
#     for j, cell in enumerate(col):
#         ret[j] += cell * f[i]
# print(ret)
# print(np.array([np.sum(np.array([[cell * f[i] for j, cell in enumerate(col)] for i, col in enumerate(d)])[:, i]) for i in range(len(a))]))

# print(list(map(lambda x: sum(x)/len(x), zip(*list(map(lambda y: list(map(lambda z: sum(y + z), list(zip(*d)))), list(zip(*e))))))))

# print(list(map(lambda x: list(map(lambda y: sum(x + y) / (len(x)+len(y)), list(zip(*d)))), list(zip(*e)))))

# print(list(map(lambda x: list(map(lambda y: x + y, list(zip(*d)))), list(zip(*e)))))

# print(list(map(lambda x: print(x), list(zip(*d, *e)))))

# print(list(map(lambda x: sum(x) / len(x), list(zip(*d, *e)))))

# print(list(zip(a, b, c)))

# arr1 = list(map(lambda x: sum(x), list(zip(*d))))
# arr2 = list(map(lambda x: sum(x) / len(x), list(zip(*d))))
# arr3 = list(map(lambda x: max(x), list(zip(*d))))

# # arr4 = list(map(lambda x, y: print(x + ' ' + y), list(zip(*d)), list(zip(*e))))

# print(arr1)
# print(arr2)
# print(arr3)
# print(arr4)


# test = {
#     're' : [2, 3, 4],
#     'te' : [6, 8, 9],
#     'as' : [6, 2, 8]
# }

# all_tests = {'re', 'te', 'e'}


# print(list(filter(lambda x: x in test.keys(), all_tests)))

# print(list(map(lambda x: test[x], list(filter(lambda x: x in test.keys(), all_tests)))))


# import wikipedia

# s = 'dasdasdsadasd'

# page = wikipedia.page(s)

# wikipedia

# print(s)


def get_n_grams(query):
    n_grams = []
    split = query.split()
    for i in range(len(split)):
        j = i + 1
        while j <= len(split):
            n_gram = '_'.join(split[i:j])
            n_grams.append(n_gram)
            j += 1
    return n_grams

from in_out import InOut as IO

dictio = IO.read_json('./data/dictionaries/rdf2vec_large.json')

queries = IO.read_json('./data/dictionaries/queries.json')

entities = {}
for i, query in queries.items():
    entities[i] = []
    n_grams = get_n_grams(query)
    for n_gram in n_grams:
        if n_gram in dictio.keys():
            entities[i].append(n_gram)

print(entities)