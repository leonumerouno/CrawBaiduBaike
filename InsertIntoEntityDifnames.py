import requests
import csv
import pymysql

with (open(r"C:\Users\ElNum\Desktop\final_people.csv", 'r',encoding="UTF-8") as f):
    cnt = 0
    list = []
    res = []

    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        port=3306,
        database='knowledge'
    )

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    reader = csv.reader(f, delimiter=',')

    sql_insert = 'insert into knowledge.name_difnames(name,name_difname) values(%s,%s)'
    sql_query = 'select name_difname from knowledge.name_difnames'

    for row in reader:
        if cnt > 20000:
            break
        cursor.execute(sql_query)
        result = cursor.fetchall()

        str = row[0]
        if str in result or (str.count('[') == 0):
            continue
        else:
            end = str.index('[')
            strmain = str[0:end]


        if str not in list:
            list.append(str)
            try:
                cursor.execute(sql_insert,(strmain,str))
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)
        cnt+=1
    cursor.close()
    conn.close()