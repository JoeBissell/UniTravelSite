import mysql.connector
from flask import Flask, render_template, request, session, redirect, url_for, escape, abort
from passlib.hash import sha256_crypt
import hashlib
import gc
from functools import wraps
from flask import Flask, request, render_template, url_for, jsonify, redirect
import mysql.connector
from datetime import datetime


app = Flask(__name__)   

##  database connection
def get_connection():
   conn = mysql.connector.connect(host='localhost',
                                  user='suleima2abbara',
                                  password='Suleima2abbarA14+$++',
                                  database='suleima2abbara_prj')
   return conn

##  home page
@app.route('/coachhome')         
def coachhome():    
   username = session['username']   
   return render_template('/suleima/coachhome.html', username=username)

##  checking login function
def check_login(f):
   @wraps(f)
   def wrap(*args, **kwargs):
      if ('logged_in' not in session):
         return f(*args, **kwargs)
      else: 
         return render_template('suleima/coachhome.html', error= 'Already logged in')
   return wrap

##  registration success 
@app.route("/regsuccess", methods=['POST', 'GET']) 
def regsuccess():
    username = session['username']
    return render_template('/suleima/regsuccess.html')

##  registration page
@app.route('/coachreg', methods=['POST', 'GET'])
def coachreg():
   error = ''
   print('starting registration')
   try:
      if request.method == "POST":
         username = request.form['username']
         password = request.form['password']
         email = request.form['email']
         if username != None and password != None and email != None:
            conn = get_connection()
            if conn != None: 
               if conn.is_connected(): 
                  print ('database connection success')
                  dbcursor = conn.cursor()
                  password = sha256_crypt.hash((str(password)))
                  Verify_Query = "SELECT * FROM coachusers WHERE username = %s;"
                  dbcursor.execute(Verify_Query,(username,))
                  print ("SELECT query executed.")
                  rows = dbcursor.fetchall()
                  if dbcursor.rowcount > 0:
                     print ('Username taken.')
                     error = "Username already taken."
                     return render_template("suleima/coachreg.html", error=error)
                  else:
                     dbcursor.execute("INSERT INTO coachusers (username, password_hash,  email) VALUES (%s, %s, %s)", (username, password, email))
                     conn.commit()
                     print("INSERT query executed. registration is completed.")
                     dbcursor.close()
                     conn.close()
                     gc.collect()
                     return render_template("suleima/regsuccess.html", username=username)
               else:
                  error = "connection error."
                  return render_template("suleima/coachreg.html", error=error)
            else: 
               error = "Connection error."
               return render_template("suleima/coachreg.html", error=error)
         else:
            print('Empty parameters.')
            return render_template("suleima/coachreg.html", error=error)
   except Exception as e:
      return render_template("suleima/coachreg.html", error=e)
   return render_template("suleima/coachreg.html", error=error)

##  log in page
@app.route('/coachlogin', methods=["GET", "POST"])
def coachlogin():
   form={}
   error = ''
   try:
      if request.method == "POST":
         username = request.form['username']
         password = request.form['password']
         print('login in progress')
         if username !=None and password != None:
            conn = get_connection()
            if conn != None:
               if conn.is_connected():
                  print('connection to database successful')
                  dbcursor = conn.cursor()
                  dbcursor.execute("SELECT password_hash, usertype, userid FROM coachusers WHERE username = %s;", (username,))
                  data = dbcursor.fetchone()
                  if dbcursor.rowcount < 1:
                     error = "Username or password incorrect"
                     return render_template("suleima/coachlogin.html", error=error)
                  else:
                     if sha256_crypt.verify(request.form['password'], str(data[0])):
                        session['logged_in'] = True
                        session['username'] = request.form['username']
                        session['usertype'] = str(data[1])
                        session['userid'] = str(data[2])
                        print("Already logged in.")
                        if session['usertype'] == 'admin':
                           return render_template("suleima/c_admin.html", username=username, data='user specific data', usertype=session['usertype'], userid=session['userid'])
                        else: 
                           return render_template("suleima/loginsuccess.html", username=username, data='user specific data', usertype=session['usertype'], userid=session['userid'])
                     else:
                        error = "Invalid login 1."
               gc.collect()
               return render_template("suleima/coachlogin.html", form=form, error=error)
   except Exception as e:
      error = str(e) + "Invalid login 2."
      render_template("suleima/coachlogin.html", form=form, error=error)
   return render_template("suleima/coachlogin.html", form=form, error=error)

##  log out successful
@app.route('/coachlogout')
def coachlogout():
   session.clear()
   print("Logged out.")
   gc.collect()
   return render_template('/suleima/coachhome.html')

##  login successful
@app.route("/loginsuccess", methods=['POST', 'GET']) 
def loginsuccess():
    username=request.form['username']
    return render_template('/suleima/loginsuccess.html', username=username)

##  login required function
def login_req(f):
   @wraps(f)
   def wrap(*args, **kwargs):
      if 'logged_in' in session:
         return f(*args, **kwargs)
      else:
         print("Login required.")
      return render_template("suleima/coachlogin.html", error="please login first")
   return wrap

##  admin login required function
def admin_req(f):
   @wraps(f)
   def wrap(*args, **kwargs):
      if ('logged_in' in session) and (session['usertype'] == 'admin'):
         return f(*args, **kwargs)
      else:
         print("admin login required.")
   return wrap

##  coach routes lookup page
@app.route("/coachbook", methods=['POST', 'GET']) 
@login_req
def coachbook():
   username = session['username']
   conn = get_connection()
   print('databade connection successful')                          
   dbcursor = conn.cursor()                
   dbcursor.execute('SELECT DISTINCT deptCity FROM coachroutes3;')   
   print('SELECT statement executed successfully.')             
   rows = dbcursor.fetchall()                                    
   dbcursor.close()              
   conn.close() 
   cities = []
   for city in rows:
      city = str(city).strip("(")
      city = str(city).strip(")")
      city = str(city).strip(",")
      city = str(city).strip("'")
      cities.append(city)
   return render_template('/suleima/coachbook.html', username=username, departurelist=cities)

##  showing cities 
@app.route ('/arrivalcoach/', methods = ['POST', 'GET'])
@login_req
def ajax_returncoach():   
	print('/arrivalcoach') 
	if request.method == 'GET':
		deptcity = request.args.get('q')
		conn = get_connection()
		if conn != None:            
			print('MySQL Connection is established')                          
			dbcursor = conn.cursor()              
			dbcursor.execute('SELECT DISTINCT arrivCity FROM coachroutes3 WHERE deptCity = %s;', (deptcity,))   
			print('SELECT arrival statement executed successfully.')             
			rows = dbcursor.fetchall()
			total = dbcursor.rowcount                                    
			dbcursor.close()              
			conn.close() 		
			return jsonify(returncities=rows, size=total)
		else:
			print('DB connection Error')
			return jsonify(returncities='DB Connection Error')

##  booking process
@app.route ('/select-coach/', methods = ['POST', 'GET'])
@login_req
def select_coach():
      username = session['username']
      if request.method == 'POST':
         print('selecting booking')
         departcity = request.form['departureslist']
         arrivalcity = request.form['arrivalslist']
         outdate = request.form['outdate']
         adultseats = request.form['adultseats']
         childseats = request.form['childseats']
         lookupdata = [departcity, arrivalcity, outdate, adultseats, childseats]
         print(lookupdata)
         conn = get_connection()
         if conn != None:            
            print('database connection successful')                          
            dbcursor = conn.cursor()              
            dbcursor.execute('SELECT * FROM coachroutes3 WHERE deptCity = %s AND arrivCity = %s;', (departcity, arrivalcity))   
            print('SELECT statement executed successfully.')             
            rows = dbcursor.fetchall()
            datarows=[]			
            for row in rows:
               data = list(row)                    
               fare = (float(row[5]) * float(adultseats)) + (float(row[5]) * 0.5 * float(childseats))
               print(fare)
               data.append(fare)
               print(data)
               datarows.append(data)			
            dbcursor.close()              
            conn.close() 
            print(datarows)
            print(len(datarows))			
            return render_template('/suleima/c_bookstart.html', resultset=datarows, lookupdata=lookupdata, username=username)
         else:
            print('DB connection Error')
            return redirect(url_for('suleima/coachhome.html'))

##  booking confirmation
@app.route ('/c_confirm/', methods = ['POST', 'GET'])
@login_req
def c_confirm():
      if request.method == 'POST':		
         print('booking confirmation starting')
         journeyid = request.form['bookingchoice']		
         departcity = request.form['deptcity']
         arrivalcity = request.form['arrivcity']
         outdate = request.form['outdate']
         adultseats =request.form['adultseats']
         childseats =request.form['childseats']
         totalfare = request.form['totalfare']
         cardnumber = request.form['cardnumber']
         userid = session['userid']
         username = session['username']

         totalseats = int(adultseats) + int(childseats)
         bookingdata = [journeyid, departcity, arrivalcity, outdate, adultseats, childseats, totalfare, userid]
         print(bookingdata)
         conn = get_connection()
         if conn != None:    #Checking if connection is None         
            print('MySQL Connection is established')                          
            dbcursor = conn.cursor()    #Creating cursor object     	
            dbcursor.execute('INSERT INTO c_bookings3 (deptDate, idRoutes, noOfSeats, totFare, userid) VALUES \
               (%s, %s, %s, %s, %s);', (outdate, journeyid, totalseats, totalfare, userid))   
            print('INSERT statement executed successfully.')             
            conn.commit()	  
            dbcursor.execute('SELECT LAST_INSERT_ID();')
            print('SELECT statement executed successfully.')             
            rows = dbcursor.fetchone()
            bookingid = rows[0]
            bookingdata.append(bookingid)
            dbcursor.execute('SELECT * FROM coachroutes3 WHERE idRoutes = %s;', (journeyid,))   			
            rows = dbcursor.fetchall()
            deptTime = rows[0][2]
            arrivTime = rows[0][4]
            bookingdata.append(deptTime)
            bookingdata.append(arrivTime)
            print(bookingdata)
            print(len(bookingdata))
            cardnumber = cardnumber[-4:-1]
            print(cardnumber)
            dbcursor.execute
            dbcursor.close()              
            conn.close()
            return render_template('suleima/c_confirm.html', username=username, userid=userid, resultset=bookingdata, cardnumber=cardnumber)
         else:
            print('DB connection Error')
            return redirect(url_for('index'))

##  reciept 
@app.route ('/dumpsVar/', methods = ['POST', 'GET'])
def dumpVar():
	if request.method == 'POST':
		result = request.form
		output = "<H2>Data Received: </H2></br>"
		output += "Number of Data Fields : " + str(len(result))
		for key in list(result.keys()):
			output = output + " </br> " + key + " : " + result.get(key)
		return output
	else:
		result = request.args
		output = "<H2>Data Received: </H2></br>"
		output += "Number of Data Fields : " + str(len(result))
		for key in list(result.keys()):
			output = output + " </br> " + key + " : " + result.get(key)
		return output  

## view old bookings
@app.route('/c_viewbkings', methods=['GET', 'POST'])
@login_req
def c_viewbkings():
   conn = get_connection()
   if conn != None:
      if conn.is_connected():
         userid = session['userid']
         username = session['username']
         print('database connection successful')
         dbcursor = conn.cursor()
         dbcursor.execute('SELECT * FROM c_bookings3 WHERE userid = %s;', (userid,))
         print('SELECT bookings executed.')
         bookingrows = dbcursor.fetchall()
         dbcursor.close()
         conn.close()
         if not bookingrows:
            error = 'there are no bookings available'
            print(error)
            return render_template('suleima/coachhome.html', error=error)
         else:
            print(bookingrows)
            return render_template('suleima/c_viewbkings.html', bookingresult=bookingrows, userid=userid, username=username)
      else:
         error = "Connection error."
         print(error)
         return render_template("suleima/coachhome.html", error=error)
   else:
         error = "Connection error."
         print(error)
         return render_template("suleima/coachhome.html", error=error)


##  delete bookings
@app.route('/c_cancelbking', methods=['POST', 'GET'])
@login_req
def c_cancelbking():
   if request.method == 'GET':
      bookingid = request.args.get('deletebooking')
      if bookingid != None:
         conn=get_connection()
         if conn != None:
            if conn.is_connected():
               print('Connected to DB.')
               dbcursor = conn.cursor()
               sql_statement = 'DELETE FROM c_bookings3 WHERE idBooking = %s'
               args = (bookingid,)
               dbcursor.execute(sql_statement, args)
               print('DELETE statement executed.')
               conn.commit()
               dbcursor.close()
               conn.close()
               error = 'the booking has been canceled'
               print(error)
               return render_template('suleima/coachhome.html', error=error)
            else:
               print('Connection error.')
         else:
            error = "Connection error."
            print(error)
            return render_template("suleima/coachhome.html", error=error)
      else:
         error = "there are no bookings available"
         print(error)
         return render_template('suleima/coachhome.html', error=error)



##  admin login page
@app.route('/c_admin')
@admin_req
def c_admin():
   return render_template('suleima/c_admin.html')

##  admin viewing all routes
@app.route('/c_adminroutes')
@admin_req
def c_adminroutes():
   conn = get_connection()
   if conn != None:
      if conn.is_connected():
         print('Connected to DB.')
         dbcursor = conn.cursor()
         dbcursor.execute('SELECT * FROM coachroutes3;')
         print('SELECT executed.')
         rows = dbcursor.fetchall()
         dbcursor.close()
         conn.close()
         return render_template('suleima/c_adminroutes.html', resultset=rows)
      else:
         error = "error"
         return render_template("suleima/coachhome.html", error=error)
   else:
         error = "error"
         return render_template("suleima/coachhome.html", error=error)



##  admin deleting coach route
@app.route('/c_admindelete', methods=['POST', 'GET'])
@admin_req
def c_admindelete():
   if request.method == 'GET':
      routeid = request.args.get('removeroute')
      if routeid != None:
         conn=get_connection()
         if conn != None:
            if conn.is_connected():
               print('database connection successful')
               dbcursor = conn.cursor()
               sql_statement = 'DELETE FROM coachroutes3 WHERE idRoutes = %s'
               args = (routeid,)
               dbcursor.execute(sql_statement, args)
               print('DELETE executed.')
               conn.commit()
               dbcursor.close()
               conn.close()
               msg = 'coach route deleted'
               return render_template('suleima/c_admin.html', msg=msg)
            else:
               print('error')
         else:
            error = "error"
            return render_template("suleima/c_admin.html", error=msg)
      else:
         error="error"
         return render_template('suleima/c_admin.html', error=msg)

##  admin insert route form page
@app.route('/c_admininsert')
@admin_req
def c_admininsert():
   return render_template('suleima/c_admininsert.html')

##  admin add route
@app.route('/admininsert',  methods=['POST', 'GET'])
@admin_req
def admininsert():
      msg=""
      print('adding coach route starting.')
      if request.method == 'POST':
            idroute = request.form['idroute']
            leaving = request.form['departure']
            leavingtime = request.form['deptime']
            arrival = request.form['arrival']
            arrivaltime = request.form['arrivaltime']
            price = request.form['price']
            conn = get_connection()
            if conn.is_connected():
               cursor = conn.cursor()
               print("connected to database successful")
               sql_statement = "INSERT INTO coachroutes3 (idRoutes, deptCity, deptTime, arrivCity, arrivTime, stFare) VALUES (%s, %s, %s, %s, %s, %s);"
               args = (idroute, leaving, leavingtime, arrival, arrivaltime, price)
               cursor.execute(sql_statement, args)
               print("INSERT executed.")
               conn.commit()
               cursor.close()
               msg = "route added successfully"
               print(msg)
               return render_template('suleima/c_admin.html', msg= msg)
            else:
               conn.rollback()
               msg += "Error while inserting"
               print(msg)
               return render_template('suleima/c_admin.html', msg= msg)
      else:
         print('Not POST')
         return 'Not POST'


