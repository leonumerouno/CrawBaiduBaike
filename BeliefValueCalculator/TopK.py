from sentence_transformers import SentenceTransformer, util
import torch
import pymysql
import pickle
import Dbquery
from word_similarity import WordSimilarity2010

class TopK(object):

    def init(self):
        self.dbquery = Dbquery().Dbquery()
        self.model = SentenceTransformer("distiluse-base-multilingual-cased-v2")
        self.embedder = SentenceTransformer("bert-base-chinese")
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
        top_results = torch.topk(cos_scores, 25)

        maxBeliefValue = 0
        for score, idx in zip(top_results[0], top_results[1]):
            topk.append(corpus[idx])
            maxBeliefValue = max(maxBeliefValue,score)

        return topk,maxBeliefValue

    def WordSimilarity(self,word1,word2):
        return self.ws_tool.similarity(word1, word2)
