import pandas as pd
from whoosh.fields import *
import os.path
from whoosh.index import create_in




schema = Schema(id=TEXT(stored=True), title=TEXT(stored=True), numCols=NUMERIC(stored=True), pgTitle=TEXT(stored=True), numDataRows=NUMERIC(stored=True), secondTitle=TEXT(stored=True), numHeaderRows=NUMERIC(stored=True), caption=TEXT(stored=True), content=TEXT(stored=True))

if not os.path.exists("index"):
    os.mkdir("index")
ix = create_in("index", schema)