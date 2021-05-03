import mysql.connector
from flask import Flask, render_template, request, session, redirect, url_for, escape, abort
from passlib.hash import sha256_crypt
import hashlib
import gc
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo



app = Flask(__name__)   




def get_connection():
   conn = mysql.connector.connect(host='localhost',
                                  user='suleima2abbara',
                                  password='Suleima2abbarA14+$++',
                                  database='suleima2abbara_prj')
   return conn


## route to home page
@app.route('/coachhome')         
def coachhome():       
   return render_template('/suleima/coachhome.html')

@app.route("/coach")
def coach():
    if request.method =='POST':
        return "hello"
    else:
        return render_template("/suleima/coach.html")





