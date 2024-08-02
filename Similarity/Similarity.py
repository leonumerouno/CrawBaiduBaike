from sentence_transformers import SentenceTransformer, util
import torch
import pymysql
import pickle

embedder = SentenceTransformer("distiluse-base-multilingual-cased-v2")

conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        port=3306,
        database='knowledge'
    )

with open("embeddings.pkl", "rb") as fIn:
    stored_data = pickle.load(fIn)
    corpus = stored_data["sentences"]
    corpus_embeddings = stored_data["embeddings"]

# Query sentences:
queries = [
    "孙悦，黑龙江省哈尔滨市道外区人力资源和社会保障局党组成员、副局长、三级调研员。",
    "周洋的游戏id是fy，跟dota2的森哥一个id，但他在RA Period呆过。"
]


# Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
top_k = 5
for query in queries:
    query_embedding = embedder.encode(query, convert_to_tensor=True)

    # We use cosine-similarity and torch.topk to find the highest 5 scores
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)

    print(top_results)

    """
    # Alternatively, we can also use util.semantic_search to perform cosine similarty + topk
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=5)
    hits = hits[0]      #Get the hits for the first query
    for hit in hits:
        print(corpus[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))
    """