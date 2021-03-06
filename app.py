import mysql.connector
from flask import Flask, render_template, request, session, redirect, url_for, escape, abort, jsonify, redirect
from passlib.hash import sha256_crypt
import hashlib
import gc
from functools import wraps
from datetime import datetime
import sys

sys.path.insert(0, './flask')

#  Who's done what
#  +++++++++++++++++++++
#  + Flight - Hollie Student ID: 19041302  +
#  + Coach - Suliema Student ID: 19020111 +
#  + Taxi - Oscar Student ID: 19023984 +
#  + Car Hire - Joe Student ID: 19039830   +
#  + Train - Bradley Student ID: 20015905  +
#  +++++++++++++++++++++

app = Flask(__name__)
app.secret_key = 'verysecretkey'


## create connection to DB
def get_connection():
   conn = mysql.connector.connect(host='localhost',
                                  user='root',
                                  password='password',
                                  database='travelsite')
   return conn

def saysup():
   print("Sup Dudes")

# Import each persons python
import taxi, coach, air, carhire, Train

def sayyo():
   print("Yo Dudes")

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
app.add_url_rule('/oscarbookings/', view_func=taxi.oscarbookings, methods=['POST', 'GET'])
app.add_url_rule('/oscarreturnarrival/', view_func=taxi.ajax_returnarrival, methods=['POST', 'GET'])
app.add_url_rule('/oscarselectbooking/', view_func=taxi.oscarselectbooking, methods=['POST', 'GET'])
app.add_url_rule('/oscarbookingconfirm/', view_func=taxi.oscarbookingconfirm, methods=['POST', 'GET'])
## TAXI ADMIN
app.add_url_rule('/oscar_admininsert', view_func=taxi.oscar_admininsert)
app.add_url_rule('/oscaradmininsert', view_func=taxi.oscaradmininsert, methods=['POST', 'GET'])
app.add_url_rule('/oscar_adminroutes', view_func=taxi.oscar_adminroutes)
app.add_url_rule('/oscaradminremoveroute', view_func=taxi.oscaradminremoveroute, methods=['POST', 'GET'])
## TAXI USER MANAGEMENT
app.add_url_rule('/oscarusermanage', view_func=taxi.oscarusermanage)
app.add_url_rule('/oscaruserchangepass', view_func=taxi.oscaruserchangepass, methods = ['POST', 'GET'])
app.add_url_rule('/oscarbookingcancel', view_func=taxi.oscarbookingcancel, methods=['POST', 'GET']) 
app.add_url_rule('/oscardeletebooking/', view_func=taxi.oscardeletebooking, methods=['POST', 'GET'])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hollie")
def hollie():
    return render_template("hollie/airTravelwelcome.html")

@app.route("/bradley")
def bradley():
    return render_template("bradley/index.html")

@app.route("/suleima")
def suleima():
    return render_template("suleima/coachhome.html")



### suleima addara - 19020111 
app.add_url_rule('/coachhome', view_func=coach.coachhome)
app.add_url_rule('/coachreg', view_func=coach.coachreg, methods=['POST', 'GET'])
app.add_url_rule('/regsuccess', view_func=coach.regsuccess, methods=['POST', 'GET'])
app.add_url_rule('/coachlogin', view_func=coach.coachlogin, methods=['POST', 'GET'])
app.add_url_rule('/loginsuccess', view_func=coach.loginsuccess, methods=['POST', 'GET'])
app.add_url_rule('/coachlogout', view_func=coach.coachlogout, methods=['POST', 'GET'])
app.add_url_rule('/coachbook', view_func=coach.coachbook, methods=['POST', 'GET'])
app.add_url_rule('/arrivalcoach/', view_func=coach.ajax_returncoach, methods=['POST', 'GET'])
app.add_url_rule('/select-coach/', view_func=coach.select_coach, methods=['POST', 'GET'])
app.add_url_rule('/c_confirm/', view_func=coach.c_confirm, methods=['POST', 'GET'])
app.add_url_rule('/dumpsVar/', view_func=coach.dumpVar, methods=['POST', 'GET'])
app.add_url_rule('/c_viewbkings/', view_func=coach.c_viewbkings, methods=['POST', 'GET'])
app.add_url_rule('/c_cancelbking/', view_func=coach.c_cancelbking, methods=['POST', 'GET'])
app.add_url_rule('/c_admin', view_func=coach.c_admin)
app.add_url_rule('/c_adminroutes', view_func=coach.c_adminroutes)
app.add_url_rule('/c_admindelete', view_func=coach.c_admindelete, methods=['POST', 'GET'])
app.add_url_rule('/c_admininsert', view_func=coach.c_admininsert)
app.add_url_rule('/admininsert', view_func=coach.admininsert, methods=['POST', 'GET'])









##??HOLLIE'S AIR TRAVEL APP
# HOMEPAGE, LOGIN, SIGN UP AND REGISTER APP ROUTES
app.add_url_rule('/airtravelhome', view_func=air.airtravelhome)
app.add_url_rule('/airtravelsuccessreg', view_func=air.airtravelsuccessreg, methods=['POST', 'GET'])
app.add_url_rule('/registerairtravel', view_func=air.registerairtravel, methods=['POST', 'GET'])
app.add_url_rule('/airtravellogin', view_func=air.airtravellogin, methods=['POST', 'GET'])
app.add_url_rule('/logoutairtravel', view_func=air.logoutairtravel, methods=['POST', 'GET'])
app.add_url_rule('/successairlogin', view_func=air.successairlogin, methods=['POST', 'GET'])
# BOOKING ROUTES
app.add_url_rule('/airtravelbooking', view_func=air.airtravelbooking, methods=['POST', 'GET'])
app.add_url_rule('/airtravelarrival/', view_func=air.ajax_returnairtravel, methods=['POST', 'GET'])
app.add_url_rule('/airtravelbookingselect/', view_func=air.airtravelbooking_select, methods=['POST', 'GET'])
app.add_url_rule('/airtravelbookingconfirm/', view_func=air.airtravelbooking_confirm, methods=['POST', 'GET'])
app.add_url_rule('/varDump/', view_func=air.varDump, methods=['POST', 'GET'])
# ADMIN ROUTES
app.add_url_rule('/air_admin', view_func=air.air_admin)
app.add_url_rule('/air_routesadmin', view_func=air.air_routesadmin)
app.add_url_rule('/air_deleteadmin', view_func=air.air_deleteadmin, methods=['POST', 'GET'])
app.add_url_rule('/air_insertroute', view_func=air.air_insertroute)
app.add_url_rule('/airinsertadmin', view_func=air.airinsertadmin, methods=['POST', 'GET'])

# USER ACCOUNT ROUTES
app.add_url_rule('/airtravelusermanag', view_func=air.airtravelusermanag)
app.add_url_rule('/air_viewbookings', view_func=air.air_viewbookings, methods=['POST', 'GET'])
app.add_url_rule('/air_cancelbooking/', view_func=air.air_cancelbooking, methods=['POST', 'GET'])

# BRAD APP ROUTES
#My App routes
app.add_url_rule('/Trainhome', view_func=Train.Trainhome)
app.add_url_rule('/Train', view_func=Train.Train, methods=['POST', 'GET'])

#Registration App routes
app.add_url_rule('/Trainreg', view_func=Train.Trainreg, methods=['POST', 'GET'])
app.add_url_rule('/trainregsuccess', view_func=Train.trainregsuccess, methods=['POST', 'GET'])

#Login App routes
app.add_url_rule('/Trainlogin', view_func=Train.Trainlogin, methods=['POST', 'GET'])
app.add_url_rule('/trainloginsuccess', view_func=Train.trainloginsuccess, methods=['POST', 'GET'])
app.add_url_rule('/Trainlogout', view_func=Train.Trainlogout, methods=['POST', 'GET'])

#Booking App routes
app.add_url_rule('/Trainbooking', view_func=Train.Trainbooking, methods=['POST', 'GET'])
app.add_url_rule('/Trainarrival', view_func=Train.ajax_returntraintravel, methods=['POST', 'GET'])
app.add_url_rule('/Trainselectbooking', view_func=Train.Trainselect_booking, methods=['POST', 'GET'])
app.add_url_rule('/Trainconfirmbooking', view_func=Train.Trainconfirm_booking, methods=['POST', 'GET'])
app.add_url_rule('/trainvarDump', view_func=Train.trainvarDump, methods=['POST', 'GET'])

#User features - Cancel booking and View booking
app.add_url_rule('/Train_cancelbooking', view_func=Train.Train_cancelbooking, methods=['POST', 'GET'])
app.add_url_rule('/Trainviewbook', view_func=Train.Trainviewbook, methods=['POST', 'GET'])

app.run(debug = True, port = 5000)

