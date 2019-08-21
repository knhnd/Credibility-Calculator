#!coding:utf-8
# Manage application and rooting (includes main script of the application)
from flask import Flask, render_template, request
from modules import nlp_preprocessing
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
    judge_result = nlp_preprocessing.judge_lang(target)  # judge the language type (module: nlp_preprocessing).
    keywords = ""  # This value is used for print the preprocessed target information (It's mainly used for Japanese).
    output = target  # This value is used to print final result.

# Preprocessing for English (英語の前処理) -----------------------------------------------------------------------------------------
    if judge_result == "English":  # If the target information is English,
        target = target.lower()  # change words to lowercase.
        context = nlp_preprocessing.context_en(target)  # process simple context analysis. ターゲットが伝聞推定の場合は信憑性評価をしない.
        if context == 0:  # If context is 0, It means the target is not opinion. 
            keywords = nlp_preprocessing.morpho_en(target)  # get the keywords from the target information.
            if target != "None":  # If the target are not invalid value,
                excution_flag = 1  # execution flag is 1.
        else:  # It's opinion, nothing to do.
            keywords = nlp_preprocessing.morpho_en(target)  # only print the target information.
            output = "* Error: The credibility assessment can not be processed because the credibility of this informaiton is too low."
    else:
        pass

# Preprocessing for Japanese (日本語の前処理) ---------------------------------------------------------------------------------------
    if judge_result == "Japanese":
        context = nlp_preprocessing.context_ja(target)  # 文脈判断の関数を実行し，結果を格納(断定形なら0, 伝聞・推定形なら1)
        if context == 0:  # 0は伝聞推定ではない．
            keywords = nlp_preprocessing.morpho_ja(target)  # 関数の実行結果(キーワード)を格納
            if target != "Error":  # 値が無効でなければ
                excution_flag = 2  # 前処理の結果，日本語の信憑性評価を実行
        else:  # 伝聞推定なので，キーワードだけ表示して信憑性評価は行わない
            keywords = nlp_preprocessing.morpho_ja(target)
            output = "* Error: この情報の信憑性は低いため評価を実行できませんでした．"
    else:
        pass

# Output the results -------------------------------------------------------------------------------------------------------------
    return render_template('output.html',  # output view.
        target = target,  # print input information from users.
        language = judge_result,  # print language type.
        keywords = keywords,  # print keywords.
        output = output  # print the result.
        )

if __name__=='__main__':
    app.debug = True  # debug mode ON.
    app.run(host='localhost')  # run localhost.