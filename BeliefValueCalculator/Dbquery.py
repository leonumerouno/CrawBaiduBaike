import pymysql
class Dbquery(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='123456',
            port=3306,
            database='knowledge'
        )

    def select_from_knowledge_people(self):
        sql_query = "select * from knowledge.knowledge_people"

        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql_query)

        result = cursor.fetchall()

        return result

    def select_from_knowledge_people_by_name_like(self,name):
        res = []
        sql_query = "select name from knowledge.knowledge_people where value LIKE '%" + name + "%'"

        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql_query)

        results = cursor.fetchall()

        for result in results:
            uuid = result['name']
            sentences = self.select_from_knowledge_people_by_uuid(uuid)
            for sentence in sentences:
                res.append(sentence)

        return res

    def select_from_knowledge_people_by_uuid(self, uuid):
        sql_query = "select * from knowledge.knowledge_people where name = %s"

        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql_query,(uuid))

        result = cursor.fetchall()

        return result

    def select_name_from_knowledge_people_by_uuid(self, uuid):
        sql_query = "select value from knowledge.knowledge_people where name = %s and knowledge_people.key = '中文名/姓名/名字'"

        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql_query,(uuid))

        result = cursor.fetchall()

        return result