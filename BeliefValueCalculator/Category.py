from ShortSentence import ShortSentence
class Category(object):

    def init(self):
        #条目原文
        self.text = ""
        #条目的词集，词频，词数量
        self.wordset = set()
        self.wordfreq = dict()
        self.wordnumber = 0
        #条目对应的实体
        self.entity = ""
        #条目的短句
        self.shortsentences = []

    def SetText(self,text):
        self.text = text

    def GetText(self):
        return self.text

    def SetWordSet(self, wordset):
        self.wordset = wordset

    def GetWordSet(self):
        return self.wordset

    def SetWordFreq(self, wordfreq):
        self.wordfreq = wordfreq

    def GetWordFreq(self):
        return self.wordfreq

    def SetWordNumber(self, number):
        self.wordnumber = number

    def GetWordNumber(self):
        return self.wordnumber

    def SetEntity(self,entity):
        self.entity = entity

    def GetEntity(self):
        return self.entity

    def SetShortSentences(self,sentences):
        self.shortsentences = sentences

    def GetShortSentences(self):
        return self.shortsentences
