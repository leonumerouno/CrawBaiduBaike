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

    sql = 'select upper_name from knowledge.entity_upper where entity_name = %s'
    for index,row in enumerate(reader):
        if index > 10000:
            break
        try:
            cursor.execute(sql,(row[0],row[1],row[2]))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
cursor.close()
conn.close()
