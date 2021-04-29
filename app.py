from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")

def index():
    return "Flask is running!"

app.run(debug = True, port = 5000)
