import mysql.connector
from flask import Flask, render_template, request, session, redirect, url_for, escape, abort
from passlib.hash import sha256_crypt
import hashlib
import gc
from functools import wraps

import taxi

app = Flask(__name__)

## oscar routes to taxi app ##
app.add_url_rule('/oscarindex', view_func=taxi.oscarindex)
app.add_url_rule('/oscarlookup', view_func=taxi.oscarlookup)
app.add_url_rule('/oscarregister', view_func=taxi.oscarregister,  methods=['POST', 'GET'])
app.add_url_rule('/oscarlogin', view_func=taxi.oscarlogin)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/joe")
def joe():
    return render_template("joe/index.html")

@app.route("/hollie")
def hollie():
    return render_template("hollie/index.html")

@app.route("/bradley")
def bradley():
    return render_template("bradley/index.html")

@app.route("/suleima")
def suleima():
    return render_template("suleima/coach.html")

app.run(debug = True, port = 5000)
