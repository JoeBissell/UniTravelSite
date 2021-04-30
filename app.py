from flask import Flask
from flask import render_template
import taxi


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/joe")
def joe():
    return render_template("joe/index.html")

@app.route("/oscar")
def oscar():
    return render_template("oscar/index.html")

@app.route("/hollie")
def hollie():
    return render_template("hollie/index.html")

@app.route("/bradley")
def bradley():
    return render_template("bradley/index.html")

@app.route("/suleima")
def suleima():
    return render_template("suleima/index.html")





app.run(debug = True, port = 5000)
