import csv
import pymysql
import mysql.connector

conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    passwd='123456',
    database='knowledge',
    charset="utf8")
mycursor = conn.cursor()
sql = "insert into knowledge.knowledge_sports (name,knowledge_sports.key,value,source) values (%s,%s,%s,%s)"

list_unableToInsert = ["'","//"]
list_sport = ["生日","出生日期"]
list = []

cnt = 0;
with open(r"C:\Users\ElNum\Desktop\7Lore_triple.csv", encoding='utf-8-sig') as f:
    for row in csv.reader(f, skipinitialspace=True):
        for i in list_sport:
            if row[1].find(i) != -1:
                cnt+=1
                continue
            if cnt>100000:
                break
#yago
print(cnt)



