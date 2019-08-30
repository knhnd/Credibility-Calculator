#!/usr/local/bin/python3
#_*_coding:utf-8_*_
# This is a credibility assessment module.
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
        return "No match inforamtion found. Please check about this information."  # return this alert.

# Matching target information with sensor data from database
def match_sensor(sensor_type):
    stype = sensor_type  # get sensor type.
    match = []
    result = []
    sensor_data = db_operation.get_sensor_mysql(stype)
    result = sensor_data
    return result
