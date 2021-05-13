from __main__ import app
from flask import Flask, render_template, request, session, redirect, url_for, escape, abort, jsonify, redirect


# app = Flask(__name__)

print('hi')

@app.route("/viewbookings")
def viewbookings():
    return render_template("joe/pages/viewbookings.html")

@app.route("/booktickets")
def booktickets():
    return render_template("joe/pages/makebookings.html")

@app.route("/cancelbookings")
def cancelbookings():
    return render_template("joe/pages/cancelbookings.html")

@app.route("/carhirelogin")
def carhirelogin():
    return render_template("joe/pages/login.html")