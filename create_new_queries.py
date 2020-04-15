import pickle
import pandas as pd


with open('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/query_expansion.pickle', 'rb') as handle:
      expansions = pickle.load(handle)

queries = pd.read_csv('./data/queries.csv')
queries = queries['query'].tolist()
queries = [item.strip() for item in queries]

new_queries = list()

for query in queries:
    new_query = ""
    words = query.split(" ")
    for word in words:
        new_query += word + " "
        if word in expansions:
            word_expansions = expansions[word]
            for expance in word_expansions:
                new_query += expance + " "
    print(new_query)
    new_queries.append(new_query)

output = pd.DataFrame(new_queries, columns=['query'])
print(output)
output.to_csv('./data/expanded_queries.csv')