# Flaskアプリの起動/実行などを行う管理用プログラム
from flask import *
app = Flask(__name__)  # Flaskクラスのインスタンスを生成

# 関数の実行場所を指定(複数のURLで異なる関数を動かしたいときは，@app.route()の引数の値を変更)
@app.route("/")  # URLが"/"のリクエストを受けた場合に下の関数を実行
def main():  # メイン関数
    return "It works! Hello, World!"

# caSystemを実行
@app.route("/caSystem")
def caSystem():
    return render_template('index.html')  # templateエンジンのhtmlをレンダリングして返す

if __name__ == '__main__':
    app.debug = True
app.run()
