from evaluation_BM25 import evaluate
from whoosh.scoring import BM25F
from search import search_bm25f_and, search_bm25f_or


scoring_function = BM25F(K1 = 1.5, titles_B = 0.75, caption_and_headers_B = 0.75, body_B = 0.75)
search_function_and = search_bm25f_and
search_function_or = search_bm25f_or
result_and = evaluate(search_function_and, scoring_function)
result_or = evaluate(search_function_or, scoring_function)
print("Result for and: ")
print(result_and)
print("Result for or ")
print(result_or)