import requests
import re

class WordTear(object):
    def __init__(self):
        self.url = "http://localhost/SegAPI/rest/seg"
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        }
        self.Param = {}
        self.stopwords = []

    def getStopWords(self):
        stop_words = []
        with open('cn_stopwords.txt', 'r', encoding='utf-8') as f:
            cn_stop_words = f.readlines()
        with open('scu_stopwords.txt', 'r', encoding='utf-8') as f:
            scu_stop_words = f.readlines()
        for word in cn_stop_words:
            if word not in stop_words:
                stop_words.append(word)
        for word in scu_stop_words:
            if word not in stop_words:
                stop_words.append(word)
        self.stopwords = stop_words
    def tear(self,segstr):
        self.Param = {
            'secret': 'qt80oh3psexeifkh5don6jxidicygz4ibbq5um3z',
            'segstr': segstr
        }
        resp = requests.get(self.url, params=self.Param, headers=self.header)
        split_words = resp.text.split(" ")
        wordset = set()
        wordfreq = dict()
        wordcount = 0
        for word in split_words:
            split_word = word.split("/")
            if split_word[1] != 'w' and split_word[1] not in self.stopwords:
                if split_word[0] in wordfreq:
                    wordfreq[split_word[0]] += 1
                else:
                    wordfreq[split_word[0]] = 1
                    wordset.add(split_word[0])
                wordcount += 1
        return wordset,wordfreq,wordcount

    def tear_into_words(self,segstr):
        word_list = []
        self.Param = {
            'secret': 'qt80oh3psexeifkh5don6jxidicygz4ibbq5um3z',
            'segstr': segstr
        }
        resp = requests.get(self.url, params=self.Param, headers=self.header)
        split_words = resp.text.split(" ")
        for word in split_words:
            split_word = word.split("/")
            if split_word[1] != 'w' and split_word[1] not in self.stopwords:
                word_list.append(split_word)
        return word_list

    def get_verb(self,segstr):
        verb = ""
        self.Param = {
            'secret': 'qt80oh3psexeifkh5don6jxidicygz4ibbq5um3z',
            'segstr': segstr
        }
        resp = requests.get(self.url, params=self.Param, headers=self.header)
        split_words = resp.text.split(" ")
        for word in split_words:
            split_word = word.split("/")
            if 'n' not in split_word[1]:
                verb += split_word[1]
        return verb

    def get_entity_list(self,segstr):
        entity_list = []
        self.Param = {
            'secret': 'qt80oh3psexeifkh5don6jxidicygz4ibbq5um3z',
            'segstr': segstr
        }
        resp = requests.get(self.url, params=self.Param, headers=self.header)
        split_words = resp.text.split(" ")
        for word in split_words:
            split_word = word.split("/")
            if 'n' in split_word[1]:
                entity_list.append(word)
        return entity_list