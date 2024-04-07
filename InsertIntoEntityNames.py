import requests
import csv
import pymysql

with (open(r"C:\Users\ElNum\Desktop\final_people.csv", 'r',encoding="UTF-8") as f):
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        port=3306,
        database='knowledge'
    )
    sql_insert = 'insert into knowledge.entity_names(name) values(%s)'
    sql_query = "select name from knowledge.entity_names"

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    reader = csv.reader(f, delimiter=',')

    cursor.execute(sql_query)
    result = list(cursor.fetchall())

    cnt = 0
    for row in reader:

        str = row[0]
        list = str.split('[')
        strmain = list[0]

        if strmain in result:
            continue
        else:
            try:
                cursor.execute(sql_insert,strmain)
                result.append(strmain)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)

    cursor.close()
    conn.close()