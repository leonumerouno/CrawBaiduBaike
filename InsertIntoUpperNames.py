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

    for row in reader:
        if cnt > 10000:
            break

        if str not in list:
            list.append(str)
            url = "http://shuyantech.com/api/cnprobase/concept?q=" + str
            response = requests.get(url)
            list1 = response.json()['ret']

            if len(list1) != 0:
                for i in list1:
                    if i[0] not in res:
                        sql = 'insert into knowledge.entity_upper(entity_name,upper_name) values(%s,%s)'
                        try:
                            cursor.execute(sql,(str,i[0]))
                            conn.commit()
                        except Exception as e:
                            conn.rollback()
                            print(e)
            cnt+=1
        else:
            continue
    cursor.close()
    conn.close()

