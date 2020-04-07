import os.path

import pandas as pd
from whoosh.index import create_in

from schema import schema

if not os.path.exists("index"):
    os.mkdir("index")
ix = create_in("index", schema)