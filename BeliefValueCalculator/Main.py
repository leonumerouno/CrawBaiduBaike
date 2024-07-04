from Cracking import Cracking
from TopK import TopK
from Category import Category
from WordTear import WordTear
from Dbquery import Dbquery
from ShortSentence import ShortSentence

class BeliefValueCalculator(object):
    def __init__(self):
        self.Cracking = Cracking()
        self.texts = ["周国治, 周国治，男，研究员、研究室主任，浙江省重点实验室——浙江省设施园艺工程技术研究中心主任，国家大宗蔬菜产业技术体系杭州综合试验站站长 ，1987年7月毕业于浙江农业大学；本科学历，学士学位。",
                      "二郎神, 二郎神，电视剧《远古的传说》中的角色，由演员段秋旭饰演。",
                      ""]
        self.TopK = TopK()
        #条目总list
        self.categories = []
        self.WordTear = WordTear()
        self.dbquery = Dbquery()
        self.shortsentence = ShortSentence()

    def Calculate(self):

        self.Cracking.init()
        self.TopK.init()

        # 第一步：判断相关/无关
        # Step1:获取裂解完的所有命题
        for text in self.texts:
            category = Category()
            category.SetText(text)
            #TODO:如何获取实体名？
            shorted_texts = self.cracking.process_and_format_text(text,"")
            shortsentences = []
            for shorted_text in shorted_texts:
                short_sentence_list = self.Cracking.generate_text(shorted_text)
                for sentence in short_sentence_list:
                    shortsentence = ShortSentence()
                    shortsentence.SetText(sentence)
                    shortsentences.append(shortsentence)
            category.SetShortSentences(shortsentences)

            self.categories.append(category)

        #Step2:计算Top-K 判断是否相关
        for category in self.categories:
            short_sentences = category.GetShortSentences()
            for i in range(0,len(short_sentences)):
                topk,max_cos,wordcount = self.TopK.similarity(short_sentences[i].GetText())
                short_sentences[i].setTopK(topk)
                #TODO:判断无关的cos阈值是多少？（实验方案：从0 - 1按0.0001进行枚举实验）是否可行？
                if max_cos < 0.5:
                    short_sentences[i].SetBeliefValue(0)

        #第二步：如果相关，判断条目对应的实体
        #TODO:每个条目对应多句话，每句话对应一组TOPK，一定要遍历所有的TOPK吗？
        for category in self.categories:
            total_word_number = category.getWordNumber()
            now_weight = 0.0
            entity = ""
            short_sentences = category.GetShortSentences()
            st = set()
        #Step1:条目分词
            wordset,wordfreq,wordcount = self.WordTear.tear(category.GetText())
            category.SetWordSet(wordset)
            category.SetWordfreq(wordfreq)
            category.SetWordNumber(wordcount)
        #Step2:每个句子对应的TopK中的每个实体分词
            for sentence in short_sentences:
                if sentence.GetBeliefValue() == 0:
                    continue
                topks = sentence.GetTopK()
                for topk in topks:
                    wset = set()
                    entity_name = topk.split("的")[0]
                    if entity_name in st:
                        continue
                    else:
                        st.add(entity_name)
                        results = self.dbquery.select_from_knowledge_people_limited_name(entity_name)
                        for result in results:
                            word_list = self.WordTear.tear_into_words(result)
                            for word in word_list:
                                wset.add(word_list)
        #Step3:取TopK的set和条目的set取交集，计算权值和
                    intersection_list = list(wordset & wset)
                    weight = 0.0
                    for word in intersection_list:
                        weight += word * (wordfreq[word] / total_word_number)
                    if now_weight < weight:
                        now_weight = weight
                        entity = entity_name
            category.setEntity(entity)

        #第三步:删去TopK中无关的知识
        for category in self.categories:
            short_sentences = category.GetShortSentences()
            for sentence in short_sentences:
                if sentence.GetBeliefValue() == 0:
                    continue
                topks = sentence.GetTopK()
                newtopks = []
                entity = category.GetEntity()
                for topk in topks:
                    entity_name = topk.split("的")[0]
                    if entity_name == entity:
                        newtopks.append(topk)
                category.SetTopK(newtopks)

        #第四步：查找最相似的匹配句
        #TODO:利用SBert/wordnet近义词搜索
        for category in self.categories:
            short_sentences = category.GetShortSentences()
            for sentence in short_sentences:
                if sentence.GetBeliefValue() == 0:
                    continue
                topks = sentence.GetTopK()
                bestk = ""
                text_verb = self.WordTear.get_verb(sentence.GetText())
                for topk in topks:
                    verb = self.WordTear.get_verb(topk)
                    sim = self.TopK.WordSimilarity(text_verb,verb)
                    if max_sim < sim:
                        max_sim = sim
                        bestk = topk
                sentence.SetBestK(bestk)


        #第五步：根据命名实体判断是否矛盾或相同
        #TODO:讨论如何判断
        #TODO：(1)每个命名实体都如何判断（2）怎么判断命名实体互相对应？
        for category in self.categories:
            short_sentences = category.GetShortSentences()
            for sentence in short_sentences:
                bestk = sentence.SetBestK()
                original_text = sentence.GetText()

                bestk_entity_list = self.WordTear.get_entity_list(bestk)
                original_text_entity_list = self.WordTear.get_entity_list(original_text)


















        # for





if __name__ =="__main__":

    belief = BeliefValueCalculator()

    belief.Calculate()