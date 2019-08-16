#! coding:utf-8
# Manage application and rooting (includes main script of the application)
from flask import Flask, render_template, request
app = Flask(__name__)  # Generate Flask instance.

# Decorator
@app.route('/')
def index():
    return render_template('index.html')  # first view (template file).

# Main script
@app.route('/app', methods=['POST'])  # form access by POST.
def creeibility_assessment():  # This function is the main process of credibility assessment.
    target = request.form['target']  # get the input from users.
    return render_template('output.html', input = target)


if __name__=='__main__':
    app.debug = True  # debug mode ON.
    app.run(host='localhost')  # run localhost.