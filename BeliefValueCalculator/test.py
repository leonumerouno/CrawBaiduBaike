from TopK import TopK
from WordTear import WordTear
from Dbquery import Dbquery
from EntityLink import EntityLink

# topK = TopK()
wordtear = WordTear()
dbquery = Dbquery()
entitylink = EntityLink()

queries = []
contexts = []

with open('abc.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        queries.append(line)

with open('context.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        contexts.append(line)

for i in range(0,len(queries)):
    #获取命题对应的实体
    query = queries[i]
    context = contexts[i]

    names = wordtear.get_names(query)

    # #从元命题库中获得所有同名的实体
    propositions = dbquery.select_from_knowledge_people_by_name_like(names)
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

    print(ecs)

    # real_entity_propositions = dbquery.select_from_knowledge_people_by_name(ecs)
    # real_entity_sentences = entitylink.construct_sentences(real_entity_propositions)
    #
    # real_entity_sentence,best_score = topK.Sentencesimilarity(query,real_entity_sentences)
    #
    # print(
    #     real_entity_sentence,best_score
    # )



