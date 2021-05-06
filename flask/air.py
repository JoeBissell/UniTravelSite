import mysql.connector
import hashlib
import gc
from flask import Flask, render_template, request, session, redirect, url_for, escape, abort
from passlib.hash import sha256_crypt
from functools import wraps
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

app = Flask(__name__)  

# DATABASE CONNECTION
def get_connection():
   conn = mysql.connector.connect(host='localhost',
                                  user='hollie3baker',
                                  password='Hollie3bakeR12+$++',
                                  database='hollie3baker_prj')
   return conn

# HOMEPAGE
@app.route('/airtravelhome')         
def coachhome():    
   username = session['username']   
   return render_template('/hollie/airTravelform.html', username=username)

@app.route("/airtravel", methods=['POST', 'GET']) 
def coach():
    username = session['username'] 
    return render_template('/hollie/airTravelform.html', username=username)

# LOGIN 
@app.route('/airtravellogin', methods=["GET", "POST"])
def airtravellogin():
   form={}
   error = ''
   try:
      if request.method == "POST":
         username = request.form['username']
         password = request.form['password']
         print('Login into your account please stand by')
         if username !=None and password != None:
            conn = get_connection()
            if conn != None:
               if conn.is_connected():
                  print('Connected to DB.')
                  dbcursor = conn.cursor()
                  dbcursor.execute("SELECT password_hash, usertype, airuserid FROM airusers WHERE username = %s;", (username,))
                  data = dbcursor.fetchone()
                  if dbcursor.rowcount < 1:
                     error = " The Username or Password entered is incorrect"
                     return render_template("hollie/airTravelreg.html", error=error)
                  else:
                     if sha256_crypt.verify(request.form['password'], str(data[0])):
                        session['logged_in'] = True
                        session['username'] = request.form['username']
                        session['usertype'] = str(data[1])
                        session['userid'] = str(data[2])
                        print("You have already logged in!")
                        if session['usertype'] == 'admin':
                           return render_template("hollie/admin.html", username=username, data='user specific data', usertype=session['usertype'], airuserid=session['airuserid'])
                        else: 
                           return render_template("hollie/airTravellogin.html", username=username, data='user specific data', usertype=session['usertype'], airuserid=session['airuserid'])
                     else:
                        error = "Invalid login 1."
               gc.collect()
               return render_template("hollie/airTravelsignup.html", form=form, error=error)
   except Exception as e:
      error = str(e) + "Invalid login 2."
      render_template("hollie/airTravelsignup.html", form=form, error=error)
   return render_template("hollie/airTravelsignup.html", form=form, error=error)

# LOGIN SUCCESS
@app.route("/successairlogin", methods=['POST', 'GET']) 
def successairlogin():
    username=request.form['username']
    return render_template('/hollie/airTravellogin.html')

# LOG OUT OF ACCOUNT
@app.route('/logoutairtravel')
def logoutairtravel():
   session.clear()
   print("Logged out.")
   gc.collect()
   return render_template('/hollie/airTravelform.html')

# REGISTER ACCOUNT
@app.route('/registerairtravel', methods=['POST', 'GET'])
def registerairtravel():
   error = ''
   print('Starting registration')
   try:
      if request.method == "POST":
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
                  Verify_Query = "SELECT * FROM airusers WHERE username = %s;"
                  dbcursor.execute(Verify_Query,(username,))
                  print ("MySQL statement SELECT was executed.")
                  rows = dbcursor.fetchall()
                  if dbcursor.rowcount > 0:
                     print ('Select another Username')
                     error = "Username already taken."
                     return render_template("hollie/airTravelreg.html", error=error)
                  else:
                     dbcursor.execute("INSERT INTO airusers (username, password_hash,  email) VALUES (%s, %s, %s)", (username, password, email))
                     conn.commit()
                     print("MySQL INSERT completed. Registration complete.")
                     dbcursor.close()
                     conn.close()
                     gc.collect()
                     return render_template("hollie/airTravellogin.html")
               else:
                  error = "Connection error."
                  return render_template("hollie/airTravelreg.html", error=error)
            else: 
               error = "Connection error."
               return render_template("hollie/airTravelreg.html", error=error)
         else:
            print('Empty parameters.')
            return render_template("hollie/airTravelreg.html", error=error)
   except Exception as e:
      return render_template("hollie/airTravelreg.html", error=e)
   return render_template("hollie/airTravelreg.html", error=error)

@app.route("/airtravelsuccessreg", methods=['POST', 'GET']) 
def airtravelsuccessreg():
    username = request.form['username']
    return render_template('/hollie/airTravellogin.html')