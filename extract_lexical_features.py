import pandas as pd
import re
import json
import requests
import gensim
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from nltk import word_tokenize
import wikipedia as wiki
from extract_semantic_features import *

HEADERS = ['query_id', 'query', 'table_id', 'row', 'col', 'nul', 'in_link', 'out_link', 'pgcount', 'tImp',
            'tPF', 'leftColhits', 'SecColhits', 'bodyhits', 'PMI', 'qInPgTitle', 'qInTableTitle', 'yRank',
            'csr_score', 'idf1', 'idf2', 'idf3', 'idf4', 'idf5', 'idf6', 'max', 'sum', 'avg', 'sim', 'emax',
            'esum', 'eavg', 'esim', 'cmax', 'csum', 'cavg', 'csim', 'remax', 'resum', 'reavg', ' resim',
            'query_l', 'rel']

