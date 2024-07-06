from sentence_transformers import SentenceTransformer, util
import torch
import pymysql
import pickle
import Dbquery
from word_similarity import WordSimilarity2010
import json

class TopK(object):

    def init(self):
        self.dbquery = Dbquery.Dbquery()
        self.model = SentenceTransformer("distiluse-base-multilingual-cased-v2")
        self.embedder = SentenceTransformer("distiluse-base-multilingual-cased-v2")
        self.ws_tool = WordSimilarity2010()

    def Predata(self):
        result = self.dbquery.select_from_knowledge_people()

        sentences = []
        for dict in result:
            sentence = dict['name'] + "的" + dict['key'] + "是" + dict['value']
            sentences.append(sentence)

        embeddings = self.model.encode(sentences)

        # Store sentences & embeddings on disc
        with open("embeddings.pkl", "wb") as fOut:
            pickle.dump({"sentences": sentences, "embeddings": embeddings}, fOut, protocol=pickle.HIGHEST_PROTOCOL)

    def similarity(self,query):
        topk = []
        belief_value = []

        with open("embeddings.pkl", "rb") as fIn:
            stored_data = pickle.load(fIn)
            corpus = stored_data["sentences"]
            corpus_embeddings = stored_data["embeddings"]

        #TODO:TOP-K的K应该取多少（做实验）
        query_embedding = self.embedder.encode(query, convert_to_tensor=True)

        cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
        top_results = torch.topk(cos_scores, 5)

        maxBeliefValue = 0
        beliefvalues = []
        for score, idx in zip(top_results[0], top_results[1]):
            topk.append(corpus[idx])
            beliefvalues.append(score)
            maxBeliefValue = max(maxBeliefValue,score)
        return topk,maxBeliefValue,beliefvalues

    def WordSimilarity(self,word1,word2):
        return self.ws_tool.similarity(word1, word2)


if __name__ =="__main__":
    # topk = TopK()
    # topk.init()
    # with open('abc.txt', 'r', encoding='utf-8') as f:
    #     queries = f.readlines()
    # for query in queries:
    #     realquery = query.split(" ")[1]
    #     realquerytopk,realquerybeliefvalue,beliefvalues = topk.similarity(realquery)
    #     print(realquerytopk,beliefvalues)
    fileName = 'out.txt'
    with open(fileName, 'r', encoding='utf-8') as file:
        fileData = file.readline()

    fileDataJson = json.loads(fileData)
