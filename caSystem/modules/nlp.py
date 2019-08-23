#!/usr/local/bin/python3
#_*_coding:utf-8_*_
# Preprocessing module for NLP.
import re
import nltk
import MeCab
import unicodedata
from bs4 import BeautifulSoup
from nltk.corpus import wordnet
from collections import namedtuple
from janome.tokenizer import Tokenizer

# Judge the language type (English or Japanese) --------------------------------------------------
# (module: unicodedata)
def judge_lang(text):
    for ch in text:
        word = unicodedata.name(ch)
        if "CJK UNIFIED" in word or "HIRAGANA" in word or "KATAKANA" in word:
            return("Japanese")  # If "Hiragana" or "Katakana" or "Kanji" included, It's Japanese.
    return("English")  # If not, English.

# --------------------------------------------------------------------------------------------------------------------------------
# Simple context analysis for English text by morphological analysis (modelue: nltk)
def context_en(text):
    t = nltk.word_tokenize(text)  # tokenize the text and divide by words.
    aux = []  # list that store an aux (auxiliary verb). 助動詞を格納するリスト.
    for aux_verb in nltk.pos_tag(t):  # get pos(part of speech) by nltk. 品詞タグの取得.
        if aux_verb[1] == "MD":  # get MD (Modal Verb). 助動詞を取得.
            aux.append(aux_verb[0])  # store to list.
        else:
            aux.append("NONE")  # 
    will, may, should = "will", "may", "should"  # variable to store particular AUX. 助動詞を格納する変数.
    if will in aux or may in aux or should in aux:
        return(1)  # If the target information includes above AUX, return 1. 上記の助動詞が含まれれば1.
    else:
        return(0)  # If not, return 0. 含まれなければ0を返す.

# --------------------------------------------------------------------------------------------------------------------------------
# Remove stop word by morphological analysis (module: nltk)
def morpho_en(text):
    t = nltk.word_tokenize(text)  # tokenize the text and divide by words.
    words_en = []  # list that store words
    tag_sets = ["NN", "NNS", "NNP", "NNPS", "VB", "VBP", "VBZ", "VBD", "VBN", "VBG"]  # tag set (noun and verb).
    for token in nltk.pos_tag(t):  # get pos.
        if token[1] in tag_sets:  # If the word is noun,
            words_en.append(token[0])  # store to the list.
    key_word = ', '.join(words_en)  # integrate the list.
    return(key_word)

# --------------------------------------------------------------------------------------------------------------------------------
# Simple context analysis for Japanese text by morphological analysis (modelue: re)
def context_ja(text):
    global preprocessing_result  # 結果によって値を変えるフラグ
    t = None  # targetの解析結果を入れるグローバル変数を定義しておく
    # Filtering by Regular Expression (正規表現で伝聞形，推量形は除く)
    pattern = re.compile(r'だろう|らしい|かもしれない|と思われる|だそうだ|とのこと')  # 伝聞・推定の形を手動で決めている
    match = pattern.findall(text)
    if match:
        return(1)  # 伝聞・推定形の場合1を返す
    else:
        return(0)  # 伝聞・推定形でなければ0を返す

# --------------------------------------------------------------------------------------------------------------------------------
# 形態素解析で日本語文章の名詞・動詞を抽出，ストップワードの削除 (module: MeCab)
def morpho_ja(text):
    tagger = MeCab.Tagger()  # MeCabのインスタンス
    tagger.parse('')  # 一度空の文字列をparseしないとエラー
    text_node = tagger.parseToNode(text)  # 解析
    words_ja = []  # 単語を格納するリスト．ここにtextの名詞が格納される
    while text_node:
        word = text_node.surface.split(",")[0]  # surfaceは単語を取得
        pos = text_node.feature.split(",")[0]  # featureは品詞(PartsOfSpeech)を取得
        if pos == "名詞" or pos == "動詞":  # 文章に名詞か動詞が含まれたら
            words_ja.append(word)  # その単語を取り出していく
        text_node = text_node.next  # nextで全形態素に順次アクセス
    if not words_ja:
        words_ja.append("Error")
    result = " ".join(words_ja)  # 抜き出したキーワードを文字列に変換し，空白で繋げて格納
    return result

# --------------------------------------------------------------------------------------------------------------------------------
# split string by ,(comma) and " "(space) and make list. 
def make_list(str):
    words = str.split()
    return words

# --------------------------------------------------------------------------------------------------------------------------------
# Remove URL
def clean_url(html_text):
    clean_text = re.sub(r'http\S+', '', html_text)
    return clean_text

# --------------------------------------------------------------------------------------------------------------------------------
# Normalize text
def normalize(text):
    normalized_text = normalize_unicode(text)
    normalized_text = normalize_number(normalized_text)
    normalized_text = lower_text(normalized_text)
    return normalized_text

# --------------------------------------------------------------------------------------------------------------------------------
# Normalize unicode
def normalize_unicode(text, form='NFKC'):
    normalized_text = unicodedata.normalize(form, text)
    return normalized_text

# --------------------------------------------------------------------------------------------------------------------------------
# Normalize number
def normalize_number(text):
    # 連続した数字を0で置換
    replaced_text = re.sub(r'\d+', '0', text)
    return replaced_text

# --------------------------------------------------------------------------------------------------------------------------------
# Cleaning text by regular expression
def clean_text(text):
    replaced_text = '\n'.join(s.strip() for s in text.splitlines()[2:] if s != '')  # skip header by [2:]
    replaced_text = replaced_text.lower()
    replaced_text = re.sub(r'[【】]', ' ', replaced_text)  # remove【】
    replaced_text = re.sub(r'[（）()]', ' ', replaced_text)  # remove（）
    replaced_text = re.sub(r'[［］\[\]]', ' ', replaced_text)  # remove［］
    replaced_text = re.sub(r'[@＠]\w+', '', replaced_text)  # remove @ (mention)
    replaced_text = re.sub(r'https?:\/\/.*?[\r\n ]', '', replaced_text)  # remove URL
    replaced_text = re.sub(r'　', ' ', replaced_text)  # remove space
    replaced_text = re.sub(r'\n', ' ', replaced_text)  # remove return
    return replaced_text

# --------------------------------------------------------------------------------------------------------------------------------
# Cleaning text by regular expression (custom version)
def cleaning(raw_data):
    replaced_text = raw_data
    replaced_text = re.sub(r'\n', ' ', replaced_text)  # remove return
    replaced_text = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)", '', replaced_text)  # Remove URL
    return replaced_text
