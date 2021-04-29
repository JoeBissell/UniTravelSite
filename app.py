from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")

def index():
    return render_template("index.html")

@app.route("/oscar")

def oscar():
    return render_template("oscar/index.html")



app.run(debug = True, port = 5000)
