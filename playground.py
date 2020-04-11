import pandas as pd

data = pd.read_csv('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/relevant_Tables.csv')

print(data)

data = data.drop_duplicates()
print(data)