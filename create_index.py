import pandas as pd
from whoosh.fields import *
import os.path
from whoosh.index import create_in




schema = Schema(id=TEXT, title=TEXT, numCols=NUMERIC, pgTitle=TEXT, numDataRows=NUMERIC, secondTitle=TEXT, numHeaderRows=NUMERIC, caption=TEXT, content=TEXT)

if not os.path.exists("index"):
    os.mkdir("index")
ix = create_in("index", schema)