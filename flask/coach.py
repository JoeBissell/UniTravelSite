import mysql.connector
from flask import Flask, render_template, request, session, redirect, url_for, escape, abort
from passlib.hash import sha256_crypt
import hashlib
import gc
from functools import wraps
# from flask_wtf import FlaskForm  -- Commented this out as not a module name
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

@app.route("/coach", methods=['POST', 'GET']) 
def coach():
    return render_template('/suleima/coach.html')


@app.route('/coachresult', methods=['POST', 'GET'])
def coachresult():
    leaving=request.form['leaving']
    conn = get_connection()
    if conn != None:
           print ('Connected to DB.')
           dbcursor = conn.cursor()
           SQL_statement = 'SELECT * FROM coach WHERE leaving = %s'
           args = (leaving,)
           dbcursor.execute(SQL_statement, args)
           print('SELECT executed.')
           rows = dbcursor.fetchall()
           dbcursor.close()
           conn.close()
           return render_template('suleima/coachresult.html', resultset=rows)
    else:
        return "connection failed"


@app.route("/regsuccess", methods=['POST', 'GET']) 
def regsuccess():
    username = request.form['username']
    return render_template('/suleima/regsuccess.html')

@app.route("/coachreg", methods=['POST', 'GET']) 
def coachreg():
         username = request.form['username']
         password = request.form['password']
         email = request.form['email']
         if username != None and password != None and email != None:
            conn = get_connection()
            if conn != None: 
               if conn.is_connected(): 
                  print ('Connected to DB.')
                  dbcursor = conn.cursor()
                  password = sha256_crypt.hash((str(password)))
                  Verify_Query = "SELECT * FROM coachusers WHERE username = %s;"
                  dbcursor.execute(Verify_Query,(username,))
                  print ("SELECT executed.")
                  rows = dbcursor.fetchall()
                  if dbcursor.rowcount > 0:
                     print ('Username taken.')
                     error = "Username already taken."
                     return render_template("suleima/coachreg.html", error=error)
                  else:
                     dbcursor.execute("INSERT INTO coachusers (username, password_hash,  email) VALUES (%s, %s, %s)", (username, password, email))
                     conn.commit()
                     print("INSERT executed. Registration complete.")
                     dbcursor.close()
                     conn.close()
                     gc.collect()
                     return render_template("suleima/regsuccess.html")
               else:
                  error = "Connection error."
                  return render_template("suleima/coachhome.html", error=error)
            else: 
               error = "Connection error."
               return render_template("suleima/coachhome.html", error=error)



@app.route("/coachlogin", methods=['POST', 'GET']) 
def coachlogin():
    return render_template('/suleima/coachlogin.html')

@app.route("/loginsuccess", methods=['POST', 'GET']) 
def loginsuccess():
    username=request.form['username']
    return render_template('/suleima/loginsuccess.html')

