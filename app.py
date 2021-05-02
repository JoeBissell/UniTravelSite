import mysql.connector
from flask import Flask, render_template, request, session, redirect, url_for, escape, abort, jsonify, redirect
from passlib.hash import sha256_crypt
import hashlib
import gc
from functools import wraps
from datetime import datetime

import taxi, coach

app = Flask(__name__)
app.secret_key = 'verysecretkey'

## create connection to DB
def get_connection():
   conn = mysql.connector.connect(host='localhost',
                                  user='root',
                                  password='password',
                                  database='travelsite')
   return conn

## LOG IN
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

## REGISTRATION 
@app.route('/register', methods=['POST', 'GET'])
def register():
   error = ''
   print('Register start')
   try:
      if request.method == "POST":
         username = request.form['username']
         password = request.form['password']
         email = request.form['email']
         if username != None and password != None and email != None:
            conn = get_connection()
            if conn != None: 
               if conn.is_connected(): 
                  print ('MySQL connection established')
                  dbcursor = conn.cursor()
                  password = sha256_crypt.hash((str(password)))
                  Verify_Query = "SELECT * FROM users WHERE username = %s;"
                  dbcursor.execute(Verify_Query,(username,))
                  rows = dbcursor.fetchall()
                  if dbcursor.rowcount > 0:
                     print ('username already taken')
                     error = "Username already taken"
                     return render_template("register.html", error=error)
                  else:
                     dbcursor.execute("INSERT INTO users (username, password_hash,  email) VALUES (%s, %s, %s)", (username, password, email))
                     conn.commit()
                  print("registered")
                  dbcursor.close()
                  conn.close()
                  gc.collect()
                  return render_template("registersuccess.html")
            else:
               print('Connection error')
               return 'DB connection error'
         else: 
            print ('Connection error')
            return 'DB connection error'
      else:
         print('empty parameters')
         return render_template("register.html", error=error)
   except Exception as e:
      return render_template("register.html", error=e)
   return render_template("register.html", error=error)

## OSCAR TAXI APP
app.add_url_rule('/oscarindex', view_func=taxi.oscarindex)
app.add_url_rule('/oscarlookup', view_func=taxi.oscarlookup)
app.add_url_rule('/oscar_show_route', view_func=taxi.oscar_show_route, methods=['POST','GET'])
app.add_url_rule('/oscarregister', view_func=taxi.oscarregister,  methods=['POST', 'GET'])
app.add_url_rule('/oscarlogin', view_func=taxi.oscarlogin, methods=['POST', 'GET'])
app.add_url_rule('/oscarlogout', view_func=taxi.oscarlogout)
## TAXI BOOKINGS
app.add_url_rule('/oscarbookings', view_func=taxi.oscarbookings, methods=['POST', 'GET'])
app.add_url_rule('/oscarreturnarrival/', view_func=taxi.ajax_returnarrival, methods=['POST', 'GET'])
app.add_url_rule('/oscarselectbooking/', view_func=taxi.oscarselectbooking, methods=['POST', 'GET'])
app.add_url_rule('/oscarbookingconfirm/', view_func=taxi.oscarbookingconfirm, methods=['POST', 'GET'])
app.add_url_rule('/oscarbookingcancel/', view_func=taxi.oscarbookingcancel, methods=['POST', 'GET']) 
app.add_url_rule('/oscardeletebooking/', view_func=taxi.oscardeletebooking, methods=['POST', 'GET'])
## TAXI ADMIN
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


app.add_url_rule('/coachhome', view_func=coach.coachhome)
app.add_url_rule('/coach', view_func=coach.coach)



app.run(debug = True, port = 5000)
