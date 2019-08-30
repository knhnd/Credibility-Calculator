#!/usr/local/bin/python3
#_*_coding:utf-8_*_
# Database operation module
import os, re
import json
import sqlite3
import subprocess

# Directory operation
def directory(dir_name, subdir_name):
    # 探索するディレクトリを指定("./dataset")するとループ一回毎に中のディレクトリを取得しdirへ
    # その中のサブディレクトリをリストにしてsubdirへ, その下のファイルを全てfilesへ(今回はsubdirはない)
    for dir, subdir, files in os.walk(dir_name):
        if dir == subdir_name:  # 指定したディレクトリなら(germanwings_crash, ottawa_shooting, sydney_siege)
            for file_name in files:  # 中のファイルを取得していく(全てstrなので実際のデータではない)
    return file_name

# Get json data from json file
def get_json(file_name, key, val):
    json_file = file＿name  # json file name and the path.
    json_data = json.load(open(json_file))  # open json file.
    json_key = json_data[key]  # jsonデータ内の時間(created_at)を取得
    json_value = json_data[val]  # jsonデータ内の本文(text)を取得
    json_dataset = [json_key, json_value]  # 取得したjsonデータの時間と本文をセットにする
    return json_dataset

# 指定したファイルを別のディレクトリに移動する
def data_move():
    for dir, subdir, files in os.walk("./dataset/rumors/ottawa_shooting"):  # ディレクトリを指定
        if dir.find("/source-tweet") != -1:
            dir_id = dir
            dir_id = dir_id.replace("./dataset/rumors/ottawa_shooting/", "")  # strで取得しているので正規表現で不要な部分を削除
            dir_id = dir_id.replace("/source-tweet", "")
            file_name = dir_id+".json"  # ディレクトリ名をファイル名に
            path = "./dataset/rumors/ottawa_shooting/"+dir_id+"/source-tweet/"+file_name  # 操作したいファイルまでのPATH
            move_dir = "./dataset/rumors/ottawa_shooting/"  # 移動先ディレクトリ
            cmd = ["mv", path, move_dir] # 実行する外部コマンド(subprocessはスペースを読み込めないのでリストで繋げる)
            subprocess.call(cmd)  # 外部コマンド実行
    return "Success!"
#data_move()

# db操作
def json_to_db(json_dataset):
    db = sqlite3.connect('./credibility_assessment.db')  # dbへ接続
    db.execute("insert into rumor_germanwings(time, data, source_id) values (?,?,?)", json_dataset)  # セットした json_dataset を db にinsert
    db.commit()  # 変更をデータベースに保存
    db.close()  # データベースとの接続解除
    return "Success!"
#json_to_db()

# ディレクトリ内のjsonを取得して特定のデータを取り出しdbに保存
def dir_json_db():
    # 上の関数を組み合わせる
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
                db.commit()  # 変更をデータベースに保存
                db.close()  # データベースとの接続解除
    return "Success!"
#dir_json_db()