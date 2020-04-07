from whoosh.fields import TEXT, NUMERIC, Schema

schema = Schema(
    id = TEXT(stored=True),
    title = TEXT(stored=True),
    numCols = NUMERIC(stored=True),
    pgTitle = TEXT(stored=True),
    numDataRows = NUMERIC(stored=True),
    secondTitle = TEXT(stored=True), 
    numHeaderRows = NUMERIC(stored=True),
    caption = TEXT(stored=True),
    content = TEXT(stored=True))