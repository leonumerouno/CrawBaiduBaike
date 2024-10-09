from TopK import TopK
from WordTear import WordTear
from Dbquery import Dbquery
from EntityLink import EntityLink
from Cracking import Cracking
from Calculator import Calculator
from InitialBelief import InitialBelief

#beliefvalue = a * cost1 + b * cost2
#url -> beliefValue
#url -> 爬虫 计算可信度初值所需要的数据 -> cost1
#url -> 条目内容 -> 百科页面简介

#百科页面简介 context
#百科页面简介 -> 裂解 -> queries

a = 0.5
b = 0.5

topK = TopK()
wordtear = WordTear()
dbquery = Dbquery()
entitylink = EntityLink()
cracking = Cracking()
calculator = Calculator()
initialbelief = InitialBelief()

cracking.init()
calculator.init()

urls = ["https://baike.baidu.com/item/%E5%88%98%E5%BE%B7%E5%8D%8E/20869893"]

for url in urls:
    initial_beliefvalue = initialbelief.calculate(url)

    context = initialbelief.getContext(url)

    queries = cracking.generate_texts_for_sentences(context)
    print(queries)

    for i in range(0,len(queries)):
        #获取命题对应的实体
        real_sentences = []
        best_scores = []

        query = queries[i]

        names = wordtear.get_names(query)

        answer = 0.0

        for name in names:
            # 从元命题库中获得所有同名的实体
            propositions = dbquery.select_from_knowledge_people_by_name_like(name)
            proposition_dict = entitylink.propositions_divide(propositions)
            entities = entitylink.get_entities(propositions)

            #对上下文进行拆分
            context_point = wordtear.tear_context(context)

            #进行实体链接
            res = 0.0
            ecs = ""
            for entity_name in entities:
                #对每个可能相同的实体进行拆分
                entity_point = wordtear.tear_entity(proposition_dict[entity_name])
                ans = 0.0
                for word in entity_point:
                    ans += context_point[word]
                if ans >= res:
                    res = ans
                    ecs = entity_name

            linked_propositions = dbquery.select_from_knowledge_people_by_uuid(ecs)
            name = dbquery.select_name_from_knowledge_people_by_uuid(ecs)

            if len(name) != 0:
                name = name[0]['value']
            else:
                name = ecs

            linked_sentences = topK.sentences_prepare(linked_propositions,name)

            real_sentence,best_score = topK.Sentencesimilarity(query,linked_sentences)

            real_sentences.append(real_sentence)
            best_scores.append(best_score)

        answer += calculator.calculate(input_str=query,match_sentence_list=real_sentences,sentence_point_list=best_scores)

    print(a * initial_beliefvalue + b * answer) # cost2




