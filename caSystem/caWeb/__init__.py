import os
from flask import Flask

def create_app(test_config=None):  # アプリの生成と設定
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:  # testではない時, インスタンスの設定値が存在すればそれを読み込む
        app.config.from_pyfile('config.py', silent=True)
    else:  # testの設定を読み込む
        app.config.from_mapping(test_config)

    # instanceが存在することを保証する
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # helloを返すシンプルなページ
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
