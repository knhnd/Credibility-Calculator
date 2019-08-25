#!/usr/local/bin/python3
#_*_coding:utf-8_*_
# Database operation module
import sqlite3
import mysql.connector

# Particular data retrieval from DB (get the table name and retrieve name). DB内の特定データの検索(テーブル名と検索キーワードを受け取る)
# (Module: sqlite3)
def search(table_name, keyword):
    db = sqlite3.connect('./database/credibility_assessment.db')  # connect DB.
    query = "select * from " + table_name + " where data like ?"  # query.
    cmd = db.execute(query,('%' + keyword + '%',))  # execute SQL.
    return cmd
    db.close()  # disconnect from DB.

# Get the particular data from json in directory and store the DB. ディレクトリ内のjsonを取得して特定のデータを取り出しdbに保存
# (Module: sqlite3)
def dir_json_db():
    for dir, subdir, files in os.walk("./dataset/rumors"):
        if dir == "./dataset/rumors/ottawa_shooting":
            for file_name in files:
                json_file = "./dataset/rumors/ottawa_shooting/" + file_name  # os.walkは中身を見るだけでアクセスするわけではないのでファイルにアクセスするためにはそのファイル名を指定する必要がある
                json_data = json.load(open(json_file))
                json_time = json_data["created_at"]
                json_text = json_data["text"]
                json_dataset = [json_time, json_text]
                db = sqlite3.connect('./credibility_assessment.db')
                db.execute("insert into rumor_ottawashooting(time, data) values (?,?)", json_dataset)
                db.commit()  # save change to DB.
                db.close()  # disconnect from DB.
    return "Success!"
#dir_json_db()

# Get data from credibilityDB
def get_data_mysql():
    conn = mysql.connector.connect(user='root', password='Rootpassword', host='localhost', database='credibilityDB')  # databse info.
    cur = conn.cursor()  # cusor.
    cur.execute("select source, title from news_data;")  # get source name and headline from news data. 
    data = []
    for row in cur.fetchall():
        data.append(row)
    return data
    cur.close
    cur.conn  # disconnect from DB.