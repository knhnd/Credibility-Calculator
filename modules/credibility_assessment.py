#!/usr/local/bin/python3
#_*_coding:utf-8_*_
# This is a credibility assessment module.
import json
from . import nlp
from . import db_operation

# Matching target information with RSS(NEWS) data from database 
def match_rss(string):
    keyword_list = nlp.make_list(string)  # make list from keywords to use credibility assessment.
    match = []
    result = []  # this list is for return.
    news_data = db_operation.get_data_mysql()  # get news_data(source and headlilne) from database. 
    for source in news_data:
        source_low = source[1].lower()  # replace words for lowercase.
        source_words = nlp.make_list(source_low)
        com = list(set(keyword_list) & set(source_words))  # get common words.
        if len(com)  != 0:  # if there is common word,
            match.append(source[0])  # append news source.
            match.append(source[1])  # and append headline to list.
        else:
            pass

    match_result = match  # append all matching information to result.
    if len(match_result) != 0:  # if result is not empty,
        match = iter(match)  # change type to iterator.
        for i in match:
            item = []
            item.append(i)
            item.append(next(match))
            result.append(item)
        return result  # return result.
    else:  # if result is empty,
        return "No match inforamtion found."  # return this alert.

# Matching target information with sensor data from database
def match_sensor(string):
    msensor = 0  # motion sensor
    wsensor = 0  # weather sensor
    json_file = "./dict/sensor.json"  # This json file includes keywords for trigger of sensor.
    json_data = json.load(open(json_file))  # open json file. 辞書ファイルを開く.
    words = nlp.replace(string)  # split keywords by space. ターゲット情報をスペースで分割.
    for word in words:
        if word in json_data["motion_sensor"]:
            msensor = 1
        if word in json_data["weather_sensor"]:
            wsensor = 1

    if msensor == 0 and wsensor == 0:
        stype = 3
        sensor_data = "No sensor matched." 
    elif msensor == 1 and wsensor == 1:
        stype = 0
        sensor_data = db_operation.get_sensor_mysql(stype)
    elif msensor == 1 and wsensor == 0:
        stype = 1
        sensor_data = db_operation.get_sensor_mysql(stype)
    elif msensor == 0 and wsensor == 1:
        stype = 2
        sensor_data = db_operation.get_sensor_mysql(stype)    
    return sensor_data, stype

# Calculate the ratio
def calculate(target, rss, sensor):
    message = ""
    match = 0
    length_a = len(target.split())
    for text in rss:
        match += 1
    if rss != "No match inforamtion found.":
        for text in rss:
            length_b = len(text[1])
            ratio = match / (length_a * length_b)
    else:
        ratio = 0.0
    if sensor[0] == "No sensors found." and sensor[1] != 3:
        ratio = ratio * 0
        message = "This information must be matched to sensor."
    return ratio, message

