query = set([
    'query_l',
    'idf1',
    'idf2',
    'idf3',
    'idf4',
    'idf5',
    'idf6'
])

wiki = set([
    'row',
    'col',
    'nul',
    'in_link',
    'out_link',
    'pgcount',
    'tImp',
    'tPF',
    'qInPgTitle',
    'qInTableTitle',
    'yRank'
])

web = set([
    'row',
    'col',
    'nul',
    'PMI',
    'leftColHits',
    'SecColhits',
    'bodyhits',
])

LTR = query.union(
    wiki.union(
        web
    )
)

semantics = set([
    'row',
    'col',
    'nul',
    'pmi',
    'hitsLC',
    'hitsSLC',
    'hitsB',
])

STR = LTR.union(semantics)