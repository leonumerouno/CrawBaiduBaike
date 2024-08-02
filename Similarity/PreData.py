from sentence_transformers import SentenceTransformer
import pickle
import pymysql

model = SentenceTransformer("distiluse-base-multilingual-cased-v2")

conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        port=3306,
        database='knowledge'
    )
sql_query = "select * from knowledge.knowledge_people where id between 1 and 30000"

cursor = conn.cursor(pymysql.cursors.DictCursor)
cursor.execute(sql_query)

result = cursor.fetchall()

sentences = []
for dict in result:
    sentence = dict['name'] + "的" + dict['key'] + "是" + dict['value']
    sentences.append(sentence)

embeddings = model.encode(sentences)

# Store sentences & embeddings on disc
with open("embeddings.pkl", "wb") as fOut:
    pickle.dump({"sentences": sentences, "embeddings": embeddings}, fOut, protocol=pickle.HIGHEST_PROTOCOL)

