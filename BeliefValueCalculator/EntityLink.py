from collections import defaultdict


class EntityLink(object):
    def construct(self,proposition):
        name = proposition['name']
        key = proposition['key']
        value = proposition['value']
        return name + "的" + key + "是" + value


    def propositions_divide(self,propositions):
        dict = defaultdict(list)
        for proposition in propositions:
            name = proposition['name']
            dict[name].append(self.construct(proposition))
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
