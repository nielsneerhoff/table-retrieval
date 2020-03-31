from whoosh.index import open_dir
import json
ix = open_dir("index")
writer = ix.writer()

with open('C:/Users/wybek/Documents/school/Master/Information Retrieval/project2/data/relevant_Tables_working.json', 'r', encoding='utf8') as file:
    data = json.load(file)
    for i in data:
        id = i
        print(data[i]['title'])
        title = str(data[i]['title'])
        numCols = int(data[i]['numCols'])
        pgTitle = str(data[i]['pgTitle'])
        numDataRows = int(data[i]['numDataRows'])
        secondTitle = str(data[i]['secondTitle'])
        numHeaderRows = int(data[i]['numHeaderRows'])
        caption = str(data[i]['caption'])
        data = str(data[i]['data'])
        writer.add_document(id=id, title=title, numCols=numCols, pgTitle=pgTitle, numDataRows=numDataRows, secondTitle=secondTitle, numHeaderRows=numHeaderRows, caption=caption, content=data)
    writer.commit()
