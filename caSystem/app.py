#!coding:utf-8
# Manage application and rooting (includes main script of the application)
import os
from flask import Flask, render_template, request
from modules import nlp
from modules import db_operation
from modules import credibility_assessment
app = Flask(__name__)  # Generate Flask instance.

# Decorator (root)
@app.route('/')
def index():
    return render_template('index.html')  # first view (template file).

# --------------------------------------------------------------------------------------------------------------------------------
# Main script. This function is main process of credibility assessment
@app.route('/app.py', methods=['POST'])  # form access by POST.
def creeibility_assessment():
    target = request.form['target']  # get the input from users (form).
    judge_result = nlp.judge_lang(target)  # judge the language type (module: nlp_preprocessing).
    
    # values
    keywords = ""  # This value is used for print the preprocessed target information (It's mainly used for Japanese).
    result = []  # This value is final output value.
    execution_flag = 0 # This is the flag that would change by the result of preprocessing. It judge weather the system should assess credibility or not.
    output = ""  # to print final output.
    otype = 0  # this is the flag to evaluate output type (str or list)

# Preprocessing for English (英語の前処理) -----------------------------------------------------------------------------------------
    if judge_result == "English":  # If the target information is English,
        target = target.lower()  # change words to lowercase.
        context = nlp.context_en(target)  # process simple context analysis. ターゲットが伝聞推定の場合は信憑性評価をしない.
        if context == 0:  # If context is 0, It means the target is not opinion. 
            keywords = nlp.morpho_en(target)  # get the keywords from the target information.
            if target != "None":  # If the target are not invalid value,
                execution_flag = 1  # execution flag is 1.
        else:  # It's opinion, nothing to do.
            keywords = nlp.morpho_en(target)  # only print the target information.
            output = "* Error: The credibility assessment can not be processed because the credibility of this informaiton is too low."
    else:
        pass

# Preprocessing for Japanese (日本語の前処理) ---------------------------------------------------------------------------------------
    if judge_result == "Japanese":
        context = nlp.context_ja(target)  # 文脈判断の関数を実行し，結果を格納(断定形なら0, 伝聞・推定形なら1)
        if context == 0:  # 0は伝聞推定ではない．
            keywords = nlp.morpho_ja(target)  # 関数の実行結果(キーワード)を格納
            if target != "Error" and keywords != "Error":  # 値が無効でなければ
                execution_flag = 2  # 前処理の結果，日本語の信憑性評価を実行
            else:
                keywords = nlp.morpho_ja(target)
                output = "* Error: ターゲット情報が短すぎます．フルセンテンスで入力してください．"
        else:  # 伝聞推定なので，キーワードだけ表示して信憑性評価は行わない
            keywords = nlp.morpho_ja(target)
            output = "* Error: この情報の信憑性は低いため評価を実行できませんでした．"

# Process credibility assessment -------------------------------------------------------------------------------------------------
    if execution_flag == 1 or execution_flag == 2:
        result = credibility_assessment.match_rss(keywords)  # matching target information with rss(news) data from database.
        output = result  # matching result.
        if type(output) is list:  # if return is list,
            otype = 1  # output is list.
        else:
            otype = 0  # output is str.

# Output the results -------------------------------------------------------------------------------------------------------------
    return render_template('output.html',  # output view.
        target = target,  # print input information from users.
        language = judge_result,  # print language type.
        keywords = keywords,  # print keywords.
        otype = otype,  # which type is the value of "output" str or list.
        output = output  # print the result.
        )

if __name__=='__main__':
    app.debug = True  # debug mode ON.
    #app.run(host='localhost')  # run localhost.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))  # run heroku.