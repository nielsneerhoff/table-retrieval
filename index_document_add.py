from whoosh.index import open_dir
import json


ix = open_dir("index")
writer = ix.writer()

filename = './data/relevant_Tables_working.json'

with open(filename, 'r') as file:
    data = json.load(file)
    #print(type(data))
    for i in data:
        #print(i)
        #print(data[i])
        id = i
        title = str(data[i]['title'])
        numCols = int(data[i]['numCols'])
        pgTitle = str(data[i]['pgTitle'])
        numDataRows = int(data[i]['numDataRows'])
        secondTitle = str(data[i]['secondTitle'])
        numHeaderRows = int(data[i]['numHeaderRows'])
        caption = str(data[i]['caption'])
        content = str(data[i]['data'])
        writer.add_document(id=id, title=title, numCols=numCols, pgTitle=pgTitle, numDataRows=numDataRows, secondTitle=secondTitle, numHeaderRows=numHeaderRows, caption=caption, content=content)
writer.commit()

