from flask import Flask, render_template
app = Flask(__name__)  # Generate Flask instance.

# Decorator (root)
@app.route('/')
def index():
    return render_template('index.html')  # template file.

if __name__=='__main__':
    app.debug = True  # debug mode ON.
    app.run('host=localhost')