from collections import defaultdict

from Dbquery import Dbquery
dbquery = Dbquery()

class EntityLink(object):
    def construct(self,proposition,name):
        key = proposition['key']
        value = proposition['value']
        return name + "的" + key + "是" + value

    def propositions_divide(self,propositions):
        dict = defaultdict(list)
        for proposition in propositions:
            uuid = proposition['name']
            name = dbquery.select_name_from_knowledge_people_by_uuid(uuid)
            if len(name) != 0:
                name = name[0]['value']
            else:
                name = uuid
            dict[uuid].append(self.construct(proposition,name))
        return dict

    def get_entities(self,propositions):
        st = set()
        for proposition in propositions:
            st.add(proposition['name'])
        return st

    def construct_sentences(self,propositions):
        list = []
        for proposition in propositions:
            list.append(self.construct(proposition))
        return list


