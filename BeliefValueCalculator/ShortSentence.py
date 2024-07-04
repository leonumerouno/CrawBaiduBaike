class ShortSentence(object):
    def __init__(self):
        #短句对应的TopK
        self.TopK = []
        #短句对应的可信度值
        self.belief_value = 1
        #短句的文本
        self.text = ""
        self.bestK = ""

    def SetTopK(self, topk):
        self.TopK = topk

    def GetTopK(self):
        return self.TopK

    def SetBestK(self, bestk):
        self.bestK = bestk

    def GetBestK(self):
        return self.bestK

    def SetBeliefValue(self, belief_value):
        self.belief_value = belief_value

    def GetBeliefValue(self):
        return self.belief_value

    def SetText(self, text):
        self.text = text

    def GetText(self):
        return self.text

