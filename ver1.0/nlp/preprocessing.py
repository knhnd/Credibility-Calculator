#/usr/bin/python3
#_*_coding:utf-8_*_
# 信憑性計測システムの前処理で行う自然言語処理
import re
import MeCab
# input text--------------------------------------------------------------------
text = "東京都で震度5の地震"  # 入力を受け取る
def preprocessing(text):
    t = None  # textの解析結果を入れるグローバル変数を定義しておく
# Filtering by Regular Expression (正規表現で伝聞形，推量形は除く)--------------------
    pattern = re.compile(r'だろう|らしい|かもしれない|と思われる|だそうだ|とのこと')
    match = pattern.findall(text)
    if match:
        print("\nError.\nBecause of the form of this text, the system cannot assess credibility. ")
        exit()
        
# Morphological Analysis (日本語文章の名詞を抽出)-----------------------------------
    def preprocessing(text):
        tagger = MeCab.Tagger()  # MeCabのインスタンス
        tagger.parse('')  # 一度空の文字列をparseしないとエラー
        text_node = tagger.parseToNode(text)  # 解析
        words = []  # 単語を格納するリスト．ここにtextの名詞が格納される．
        while text_node:
            word = text_node.surface.split(",")[0]  # surfaceは単語を取得
            pos = text_node.feature.split(",")[0]  # featureは品詞(PartsOfSpeech)を取得
            if pos == "名詞":  # 文章に名詞が含まれたら，その単語を取り出す
                words.append(word)
            text_node = text_node.next  # nextで全形態素に順次アクセス
        result = " ".join(words)  # 抜き出したキーワードを文字列に変換し，空白で繋げて格納
        return result
    t = preprocessing(text)
    print("Element: " + t + "\n")
