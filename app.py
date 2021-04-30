import mysql.connector
from flask import Flask, render_template, request, session, redirect, url_for, escape, abort
from passlib.hash import sha256_crypt
import hashlib
import gc
from functools import wraps

import taxi

app = Flask(__name__)
app.secret_key = 'verysecretkey'

## create connection to DB
def get_connection():
   conn = mysql.connector.connect(host='localhost',
                                  user='root',
                                  password='password',
                                  database='travelsite')
   return conn

@app.route('/login', methods=["GET", "POST"])
def login():
   form={}
   error = ''
   try:
      if request.method == "POST":
         username = request.form['username']
         password = request.form['password']
         if username !=None and password != None:
            conn = get_connection()
            if conn != None:
               if conn.is_connected():
                  print('SQL connection established')
                  dbcursor = conn.cursor()
                  dbcursor.execute("SELECT password_hash, usertype FROM users where username = %s;", (username,))
                  data = dbcursor.fetchone()
                  if dbcursor.rowcount < 1:
                     error = "Username or password incorrect"
                     return render_template("login.html", error=error)
                  else:
                     if sha256_crypt.verify(request.form['password'], str(data[0])):
                        session['logged_in'] = True
                        session['username'] = request.form['username']
                        session['usertype'] = str(data[1])
                        print("Logged in")
                        if session['usertype'] == 'admin':
                           return render_template("admin.html", username=username, data='user specific data', usertype=session['usertype'])
                        else: 
                           return render_template("loginsuccess.html", username=username, data='user specific data', usertype=session['usertype'])
                     else:
                        error = "Invalid login 1"
               gc.collect()
               return render_template("login.html", form=form, error=error)
   except Exception as e:
      error = str(e) + "Invalid login 2"
      render_template("login.html", form=form, error=error)
   return render_template("login.html", form=form, error=error)

## oscar routes to taxi app ##
app.add_url_rule('/oscarindex', view_func=taxi.oscarindex)
app.add_url_rule('/oscarlookup', view_func=taxi.oscarlookup)
app.add_url_rule('/oscar_show_route', view_func=taxi.oscar_show_route, methods=['POST','GET'])
app.add_url_rule('/oscarregister', view_func=taxi.oscarregister,  methods=['POST', 'GET'])
app.add_url_rule('/oscarlogin', view_func=taxi.oscarlogin, methods=['POST', 'GET'])
app.add_url_rule('/oscarlogout', view_func=taxi.oscarlogout)
## oscar bookings
app.add_url_rule('/oscarbookings', view_func=taxi.oscarbookings)
## oscar admin route
app.add_url_rule('/oscar_admininsert', view_func=taxi.oscar_admininsert)
app.add_url_rule('/oscaradmininsert', view_func=taxi.oscaradmininsert, methods=['POST', 'GET'])
app.add_url_rule('/oscar_adminroutes', view_func=taxi.oscar_adminroutes)
app.add_url_rule('/oscaradminremoveroute', view_func=taxi.oscaradminremoveroute, methods=['POST', 'GET'])


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
