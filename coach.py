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
                                  user='root',
                                  password='password',
                                  database='travelsite')
   return conn

## route to home page
@app.route('/coachhome')         
def coachhome():       
   return render_template('/suleima/coachhome.html')

@app.route("/coach", methods = ['GET', 'POST'])
def coach():
        return render_template("/suleima/coach.html")

    #conn = get_connection()
    #if conn != None:
    #    if conn.is_connected():
    #        print("SQL connection established")
    #        dbcursor = conn.cursor()
    #        SQL_statement = "SELECT DISTINCT leaving FROM coachroutes;"
    #       dbcursor.execute(SQL_statement)
    #        print("SELECT statement executed")
    #        rows = dbcursor.fetchall()
    #        dbcursor.close()
    #        conn.close()
    #        return render_template("/suleima/coach.html, resultset=rows")
    #    else:
    #        print("database connection error")
    #        return("database connection error")
    #else:
    #    print("database connection error")
    #    return("database connection error")

@app.route("/coachresult", methods=["GET", "POST"])
def coachresult():
    if request.method =='GET':
        leaving = request.args.get('leaving')
        if leaving != None:
            conn = get_connection()
            if conn != None:
                if conn.is_connected():
                    print ('sql connection established')
                    dbcursor = conn.cursor()
                    SQL_statement = 'SELECT * FROM coachroutes WHERE leaving = %s'
                    args = (leaving,)
                    dbcursor.execute(SQL_statement, args)
                    print('SELECT statement executed')
                    rows = dbcursor.fetchall()
                    dbcursor.close()
                    conn.close()
                    return render_template('suleima/coachresult.html', resultset=rows)
                else:
                    print('db connect error')
                    return 'db connect error'
            else:
                print('db connect error')
                return 'db connect error'
        else: 
            print('invalid route')
            return render_template('suleima/coach.html')
