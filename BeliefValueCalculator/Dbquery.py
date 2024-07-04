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

    def select_from_knowledge_people_limited_name(self,name):
        sql_query = "select * from knowledge.knowledge_people where name = " + name

        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql_query)

        result = cursor.fetchall()

        return result