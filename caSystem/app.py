#!coding:utf-8
# Manage application and rooting (includes main script of the application)
from flask import Flask, render_template, request
from modules import nlp_preprocessing
app = Flask(__name__)  # Generate Flask instance.

# Decorator
@app.route('/')
def index():
    return render_template('index.html')  # first view (template file).

# --------------------------------------------------------------------------------------------------------------------------------
# Main script. This function is main process of credibility assessment
@app.route('/app', methods=['POST'])  # form access by POST.
def creeibility_assessment():
    target = request.form['target']  # get the input from users (form).
    judge_result = nlp_preprocessing.judge_lang(target)  # judge the language type (module: nlp_preprocessing).
    keywords = ""  # This value is used for print the preprocessed target information (It's mainly used for Japanese).

# Preprocessing for English (英語版の処理) -----------------------------------------------------------------------------------------
    if judge_result == "English":  # If the target information is English,
        target = target.lower()  # change words to lowercase.
        context = nlp_preprocessing.context_en(target)  # process simple context analysis. ターゲットが伝聞推定の場合は信憑性評価をしない.
        if context == 0:  # If context is 0, It means the target is not opinion. 
            keywords = nlp_preprocessing.morpho_en(target)  # get the keywords from the target information.
            if target != "None":  # If the target are not invalid value,
                excution_flag = 1  # execution flag is 1.
        else:  # It's opinion, nothing to do.
            keywords = nlp_preprocessing.morpho_en(target)  # only print the target information.
    else:
        pass

# Preprocessing for Japanese (日本語版の処理) ---------------------------------------------------------------------------------------
    if judge_result == "Japanese":
            pass

# Output the results -------------------------------------------------------------------------------------------------------------
    return render_template('output.html',  # output view.
        target = target,  # print input information from users.
        language = judge_result,  # print language type.
        keywords = keywords,  # print keywords.
        output = target  # print the result.
        )

if __name__=='__main__':
    app.debug = True  # debug mode ON.
    app.run(host='localhost')  # run localhost.