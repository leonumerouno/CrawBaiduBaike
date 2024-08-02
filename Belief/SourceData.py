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
    def get_entity_urls(self):
        sql_query = "select url from knowledge.name_difnames where id between 1000 and 5000"

        cursor = self.conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(sql_query)
        result = cursor.fetchall()

        urls = []
        for i in result:
            urls.append(i['url'])
        return urls

    def insert_into_create_history(self,difname,url,edited_times,history_url):
        sql_insert = 'insert into knowledge.create_history(entity_name,entity_url,edited_times,create_history_url) values(%s,%s,%s,%s)'

        cursor = self.conn.cursor(pymysql.cursors.DictCursor)

        try:
            cursor.execute(sql_insert, (difname, url, edited_times, history_url))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)

    def insert_into_edit(self,editor_name,name,edit_time):
        sql_insert = 'insert into knowledge.edit(editor_name,entity_name,edit_time) values(%s,%s,%s)'

        cursor = self.conn.cursor(pymysql.cursors.DictCursor)

        try:
            cursor.execute(sql_insert, (editor_name,name,edit_time))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)

    def insert_into_editors(self, editor_name, editor_urls, passed_versions, pass_rate, special_versions, helped_people):
        sql_insert = 'insert into knowledge.editors(name,profile,passed_versions,pass_rate,special_versions,helped_people) values(%s,%s,%s,%s,%s,%s)'

        cursor = self.conn.cursor(pymysql.cursors.DictCursor)

        try:
            cursor.execute(sql_insert, (editor_name,editor_urls,passed_versions,pass_rate,special_versions,helped_people))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)