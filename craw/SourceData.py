import requests
import csv
import pymysql
class SourceData(object):
    def __init__(self):
        self.conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        port=3306,
        database='knowledge'
    )

    def get_entity_names(self):
        sql_query = "select name from knowledge.entity_names where id between 30001 and 32000"

        cursor = self.conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(sql_query)
        result = cursor.fetchall()

        names = []
        for i in result:
            names.append(i['name'])
        return names

    def insert_into_main(self,name,tags,values):
        sql_insert = 'insert into knowledge.knowledge_people(knowledge_people.name,knowledge_people.key,knowledge_people.value) values(%s,%s,%s)'

        cursor = self.conn.cursor(pymysql.cursors.DictCursor)

        for i in range(0, len(tags) - 1):
            try:
                cursor.execute(sql_insert, (name,tags[i],values[i]))
                self.conn.commit()
            except Exception as e:
                self.conn.rollback()
                print(e)

    def insert_into_difnames(self,name,difname,url):
        sql_insert = 'insert into knowledge.name_difnames(name_difnames.name,name_difnames.name_difname,name_difnames.url) values(%s,%s,%s)'

        cursor = self.conn.cursor(pymysql.cursors.DictCursor)

        try:
            cursor.execute(sql_insert, (name,difname,url))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)

    def insert_into_uppername(self,difname,uppernames):
        sql_insert = 'insert into knowledge.upper_name(upper_name.name,upper_name.upper_name) values(%s,%s)'

        cursor = self.conn.cursor(pymysql.cursors.DictCursor)

        for upper_name in uppernames:
            try:
                cursor.execute(sql_insert, (difname, upper_name))
                self.conn.commit()
            except Exception as e:
                self.conn.rollback()
                print(e)
