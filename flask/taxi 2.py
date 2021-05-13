import mysql.connector
from flask import Flask, render_template, request, session, redirect, url_for, escape, abort, jsonify, redirect
from passlib.hash import sha256_crypt
import hashlib
import gc
from functools import wraps
from datetime import datetime

app = Flask(__name__)   
app.secret_key = 'verysecretkey'

## DB CONNECT
def get_connection():
   conn = mysql.connector.connect(host='localhost',
                                  user='root',
                                  password='password',
                                  database='travelsite')
   return conn

## INDEX
@app.route('/oscarindex')         
def oscarindex():  
   if 'username' in session:
      username = session['username']
      return render_template('/oscar/index.html', username=username)              
   return render_template('/oscar/index.html')


## ALREADY LOGGED IN
def check_login(f):
   @wraps(f)
   def wrap(*args, **kwargs):
      if ('logged_in' not in session):
         return f(*args, **kwargs)
      else: 
         return render_template('oscar/index.html', error= 'Already logged in')
   return wrap

## LOG IN
@app.route('/oscarlogin', methods=["GET", "POST"])
def oscarlogin():
   form={}
   error = ''
   try:
      if request.method == "POST":
         username = request.form['username']
         password = request.form['password']
         print('Attempting login.')
         if username !=None and password != None:
            conn = get_connection()
            if conn != None:
               if conn.is_connected():
                  print('Connected to DB.')
                  dbcursor = conn.cursor()
                  dbcursor.execute("SELECT password_hash, usertype, userid FROM taxiusers where username = %s;", (username,))
                  data = dbcursor.fetchone()
                  if dbcursor.rowcount < 1:
                     error = "Username or password incorrect"
                     return render_template("oscar/login.html", error=error)
                  else:
                     if sha256_crypt.verify(request.form['password'], str(data[0])):
                        session['logged_in'] = True
                        session['username'] = request.form['username']
                        session['usertype'] = str(data[1])
                        session['userid'] = str(data[2])
                        print("Already logged in.")
                        if session['usertype'] == 'admin':
                           return render_template("oscar/admin/admin.html", username=username, data='user specific data', usertype=session['usertype'], userid=session['userid'])
                        else: 
                           return render_template("oscar/login-success.html", username=username, data='user specific data', usertype=session['usertype'], userid=session['userid'])
                     else:
                        error = "Invalid login 1."
               gc.collect()
               return render_template("oscar/login.html", form=form, error=error)
   except Exception as e:
      error = str(e) + "Invalid login 2."
      render_template("oscar/login.html", form=form, error=error)
   return render_template("oscar/login.html", form=form, error=error)

## LOG OUT
@app.route('/oscarlogout')
def oscarlogout():
   session.clear()
   print("Logged out.")
   gc.collect()
   return render_template('oscar/index.html')

## LOG IN REQUIRED
def login_req(f):
   @wraps(f)
   def wrap(*args, **kwargs):
      if 'logged_in' in session:
         return f(*args, **kwargs)
      else:
         print("Login required.")
      return render_template("oscar/login.html", error="Please login first")
   return wrap

## ADMIN LOG IN REQUIRED
def admin_req(f):
   @wraps(f)
   def wrap(*args, **kwargs):
      if ('logged_in' in session) and (session['usertype'] == 'admin'):
         return f(*args, **kwargs)
      else:
         print("Admin login required.")
         abort(401)
   return wrap

## LOOKUP ROUTES
@app.route('/oscarlookup')
def oscarlookup():
   conn = get_connection()
   if conn != None:
      if conn.is_connected():
         print('Connected to DB.')
         dbcursor = conn.cursor()
         SQL_statement = 'SELECT DISTINCT leaving FROM taxiroutes;'
         dbcursor.execute(SQL_statement)
         print('SELECT statement executed.')
         rows = dbcursor.fetchall()
         dbcursor.close()
         conn.close()
         return render_template('/oscar/lookup.html', resultset=rows)
      else:
         print('Connection error.')
         error = "Connection error."
         return render_template("oscar/index.html", error=error)
   else: 
      error = "Connection error."
      return render_template("oscar/index.html", error=error)

## LOOKUP RESULTS
@app.route('/oscar_show_route', methods=['POST','GET'])
def oscar_show_route():
   if request.method =='GET':
      leaving = request.args.get('leaving')
      if leaving != None:
         conn = get_connection()
         if conn != None:
            if conn.is_connected():
               print ('Connected to DB.')
               dbcursor = conn.cursor()
               SQL_statement = 'SELECT * FROM taxiroutes WHERE leaving = %s'
               args = (leaving,)
               dbcursor.execute(SQL_statement, args)
               print('SELECT executed.')
               rows = dbcursor.fetchall()
               dbcursor.close()
               conn.close()
               return render_template('oscar/lookup-results.html', resultset=rows)
            else:
               error = "Connection error."
               return render_template("oscar/index.html", error=error)
         else:
            error = "Connection error."
            return render_template("oscar/index.html", error=error)
      else: 
         print('Invalid route.')
         return render_template('oscar/index.html')


## ADMIN ADD ROUTE TO DB
@app.route('/oscar_admininsert')
@admin_req
def oscar_admininsert():
   return render_template('oscar/admin/admininsert.html')

## ADMIN DISPLAY ALL ROUTES
@app.route('/oscar_adminroutes')
@admin_req
def oscar_adminroutes():
   conn = get_connection()
   if conn != None:
      if conn.is_connected():
         print('Connected to DB.')
         dbcursor = conn.cursor()
         dbcursor.execute('SELECT * FROM taxiroutes;')
         print('SELECT executed.')
         rows = dbcursor.fetchall()
         dbcursor.close()
         conn.close()
         return render_template('oscar/admin/adminroutes.html', resultset=rows)
      else:
         error = "Connection error."
         return render_template("oscar/index.html", error=error)
   else:
         error = "Connection error."
         return render_template("oscar/index.html", error=error)

## ADMIN ADD ROUTE TO DB
@app.route('/oscaradmininsert', methods=['POST', 'GET'])
@admin_req
def oscaradmininsert():
   msg=""
   print('Adding route to DB.')
   if request.method == 'POST':
      try:
         leaving = request.form['leaving']
         leavingtime = request.form['leavingtime']
         arrival = request.form['arrival']
         arrivaltime = request.form['arrivaltime']
         miles = request.form['miles']
         conn = get_connection()
         if conn.is_connected():
            cursor = conn.cursor()
            sql_statement = "INSERT INTO travelsite.taxiroutes (leaving, leavingtime, arrival, arrivaltime, miles) VALUES (%s, %s, %s, %s, %s)"
            args = (leaving, leavingtime, arrival, arrivaltime, miles)
            cursor.execute(sql_statement, args)
            print("INSERT executed.")
            conn.commit()
            cursor.close()
            msg = "Record added"
         print(msg)
      except:
         conn.rollback()
         msg += "Error while inserting"
         print(msg)
      finally:
         return render_template('oscar/admin/admin.html', msg= msg)
   else:
      print('Not POST')
      return 'Not POST'

## ADMIN DELETE ROUTE
@app.route('/oscaradminremoveroute', methods=['POST', 'GET'])
@admin_req
def oscaradminremoveroute():
   if request.method == 'GET':
      routeid = request.args.get('removeroute')
      if routeid != None:
         conn=get_connection()
         if conn != None:
            if conn.is_connected():
               print('Connected to DB.')
               dbcursor = conn.cursor()
               sql_statement = 'DELETE FROM taxiroutes WHERE routeid = %s'
               args = (routeid,)
               dbcursor.execute(sql_statement, args)
               print('DELETE executed.')
               conn.commit()
               dbcursor.close()
               conn.close()
               msg = 'Record removed'
               return render_template('oscar/admin/admin.html', msg=msg)
            else:
               print('Connection error.')
         else:
            error = "Connection error."
            return render_template("oscar/index.html", error=error)
      else:
         return render_template('oscar/admin/admin.html')

## REGISTRATION
@app.route('/oscarregister', methods=['POST', 'GET'])
def oscarregister():
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
                  print ('Connected to DB.')
                  dbcursor = conn.cursor()
                  password = sha256_crypt.hash((str(password)))
                  Verify_Query = "SELECT * FROM taxiusers WHERE username = %s;"
                  dbcursor.execute(Verify_Query,(username,))
                  print ("SELECT executed.")
                  rows = dbcursor.fetchall()
                  if dbcursor.rowcount > 0:
                     print ('Username taken.')
                     error = "Username already taken."
                     return render_template("oscar/register.html", error=error)
                  else:
                     dbcursor.execute("INSERT INTO taxiusers (username, password_hash,  email) VALUES (%s, %s, %s)", (username, password, email))
                     conn.commit()
                     print("INSERT executed. Registration complete.")
                     dbcursor.close()
                     conn.close()
                     gc.collect()
                     return render_template("oscar/success.html")
               else:
                  error = "Connection error."
                  return render_template("oscar/index.html", error=error)
            else: 
               error = "Connection error."
               return render_template("oscar/index.html", error=error)
         else:
            print('Empty parameters.')
            return render_template("oscar/register.html", error=error)
   except Exception as e:
      return render_template("oscar/register.html", error=e)
   return render_template("oscar/register.html", error=error)

## BOOKINGS
@app.route('/oscarbookings')
@login_req
def oscarbookings():
      conn = get_connection()
      if conn != None:           
         print('Connected to DB.')                          
         dbcursor = conn.cursor()             
         dbcursor.execute('SELECT DISTINCT leaving FROM taxiroutes;')   
         print('SELECT executed.')             
         rows = dbcursor.fetchall()                                    
         dbcursor.close()              
         conn.close() 
         leavingcity = []
         for leaving in rows:
            leaving = str(leaving).strip("(")
            leaving = str(leaving).strip(")")
            leaving = str(leaving).strip(",")
            leaving = str(leaving).strip("'")
            leavingcity.append(leaving)
         return render_template('oscar/bookings/bookings.html', leavinglist=leavingcity)
      else:
         print('Connection error.')
         return 'Connection error.'

## BOOKINGS FETCH ARRIVALS
@app.route ('/oscarreturnarrival/', methods = ['POST', 'GET'])
@login_req
def ajax_returnarrival():   
	print('Fetching arrivals.') 
	if request.method == 'GET':
		arrival = request.args.get('q')
		conn = get_connection()
		if conn != None:          
			print('Connected to DB.')                          
			dbcursor = conn.cursor()             
			dbcursor.execute('SELECT DISTINCT arrival FROM taxiroutes WHERE leaving = %s;', (arrival,))   
			print('SELECT executed.')          
			rows = dbcursor.fetchall()
			total = dbcursor.rowcount                                    
			dbcursor.close()              
			conn.close() 		
			return jsonify(returncities=rows, size=total)
		else:
			print('Connection error.')
			return jsonify(returncities='Connection error.')

## PROCEED WITH BOOKING
@app.route ('/oscarselectbooking/', methods = ['POST', 'GET'])
@login_req
def oscarselectbooking():
   if request.method == 'POST':
      print('Booking initiated.')
      leavingcity = request.form['departureslist']
      arrivalcity = request.form['arrivalslist']
      leavedate = request.form['leavedate']
      numseats = request.form['numseats']
      username = session['username']
      lookupdata = [leavingcity, arrivalcity, leavedate, numseats]
      conn = get_connection()
      if conn != None:
         print('Connected to DB.')
         dbcursor = conn.cursor()
         dbcursor.execute('SELECT * FROM taxiroutes WHERE leaving = %s AND arrival = %s', (leavingcity, arrivalcity))
         print('SELECT executed.')
         rows = dbcursor.fetchall()
         datarows=[]
         for row in rows:
            data = list(row)
            fare = (float(row[5]))
            if numseats == '2':
               fare = fare * 2 * 1.25
            if numseats == '3':
               fare = fare * 3 * 1.25
            if numseats == '4':
               fare = fare * 4 * 1.3
            data.append(fare)
            datarows.append(data)
         dbcursor.close()
         conn.close()
         return render_template('oscar/bookings/booking_start.html', username=username, resultset=datarows, lookupdata=lookupdata)
      else:
         print('Connection error.')
         return redirect(url_for('index'))

## BOOKING CONFIRM
@app.route('/oscarbookingconfirm/', methods=['POST', 'GET'])
@login_req
def oscarbookingconfirm():
   if request.method == 'POST':
      print('Booking initiated.')
      routeid = request.form['bookingchoice']
      bookingid = request.form['bookingchoice']
      departcity = request.form['leavecity']
      arrivalcity = request.form['arrivalcity']
      leavedate = request.form['leavedate']
      numseats = request.form['numseats']
      totalfare = request.form['totalfare']
      cardnumber = request.form['cardnumber']
      userid = session['userid']
      username = session['username']
      bookingdata = [routeid, bookingid, departcity, arrivalcity, leavedate, numseats, totalfare, userid]
      print(bookingdata)
      conn = get_connection()
      if conn != None:
         print ('Connected to DB.')
         dbcursor = conn.cursor()
         dbcursor.execute('INSERT INTO taxibookings (leavingdate, routeid, numseats, totalfare, userid, leaving, arrival) VALUES \
            (%s, %s, %s, %s, %s, %s, %s);', (leavedate, routeid, numseats, totalfare, userid, departcity, arrivalcity))
         print('INSERT executed.')
         conn.commit()
         dbcursor.execute('SELECT LAST_INSERT_ID();')
         rows = dbcursor.fetchone()
         bookingid = rows[0]
         bookingdata.append(bookingid)
         dbcursor.execute('SELECT * FROM taxiroutes WHERE routeid = %s', (routeid,))
         rows = dbcursor.fetchall()
         deptTime = rows[0][2]
         arrivTime = rows[0][4]
         bookingdata.append(deptTime)
         bookingdata.append(arrivTime)
         cardnumber = cardnumber[-4:-1]
         print(cardnumber)
         dbcursor.execute
         dbcursor.close()
         conn.close()
         return render_template('oscar/bookings/booking_confirm.html', username=username, resultset=bookingdata, cardnumber=cardnumber, userid=userid)
   else:
      print('Connection error.')
      error = 'Connection error.'
      return render_template('oscarindex.html', error=error)

## VIEW BOOKINGS
@app.route('/oscarbookingcancel', methods=['GET', 'POST'])
@login_req
def oscarbookingcancel():
   conn = get_connection()
   if conn != None:
      if conn.is_connected():
         userid = session['userid']
         username = session['username']
         print('Connected to DB.')
         dbcursor = conn.cursor()
         dbcursor.execute('SELECT * FROM taxibookings WHERE userid = %s;', (userid,))
         print('SELECT bookings executed.')
         bookingrows = dbcursor.fetchall()
         dbcursor.close()
         conn.close()
         if not bookingrows:
            error = 'No bookings'
            return render_template('oscar/usermanage/usermanage.html', error=error)
         else:
            return render_template('oscar/usermanage/viewbookings.html', bookingresult=bookingrows, userid=userid, username=username)
      else:
         error = "Connection error."
         return render_template("oscar/index.html", error=error)
   else:
         error = "Connection error."
         return render_template("oscar/index.html", error=error)

## DELETE BOOKING
@app.route('/oscardeletebooking', methods=['POST', 'GET'])
@login_req
def oscardeletebooking():
   if request.method == 'GET':
      bookingid = request.args.get('deletebooking')
      if bookingid != None:
         conn=get_connection()
         if conn != None:
            if conn.is_connected():
               print('Connected to DB.')
               dbcursor = conn.cursor()
               sql_statement = 'DELETE FROM taxibookings WHERE bookingid = %s'
               args = (bookingid,)
               dbcursor.execute(sql_statement, args)
               print('DELETE executed.')
               conn.commit()
               dbcursor.close()
               conn.close()
               msg = 'Record removed'
               return render_template('oscar/index.html', msg=msg)
            else:
               print('Connection error.')
         else:
            error = "Connection error."
            return render_template("oscar/index.html", error=error)
      else:
         error = "No bookings"
         return render_template('oscar/index.html', error=error)

## ACCOUNT MANAGEMENT
@app.route('/oscarusermanage')
@login_req
def oscarusermanage():
   return render_template('oscar/usermanage/usermanage.html')

## USER CHANGE PASSWORD
@app.route('/oscaruserchangepass', methods=['POST','GET'])
@login_req
def oscaruserchangepass():
   username = session['username']
   if request.method == 'POST':
      password = request.form['password']
      newPassword = request.form['newPassword']
      if password != None and newPassword != None:
         conn = get_connection()
         if conn != None:
            print('Connected to DB.')
            dbcursor = conn.cursor()
            dbcursor.execute("SELECT password_hash FROM taxiusers WHERE username = %s;", (username,))
            print('SELECT executed.')
            storedPassword = dbcursor.fetchone()
            print(storedPassword)
            if sha256_crypt.verify(request.form['password'], str(storedPassword[0])):
               newPassword = sha256_crypt.hash((str(newPassword)))
               dbcursor.execute("UPDATE taxiusers SET password_hash = %s WHERE username = %s;",(newPassword, username,))
               print('UPDATE executed.')
               conn.commit()
               dbcursor.close()
               conn.close()
               gc.collect()
               return render_template('oscar/usermanage/userchangepass.html')
            else:
               error="Invalid password"
               return render_template('oscar/usermanage/userchangepass.html', error=error)
         else:
            print('Connection error.')
            return ('Connection error.')
      else:
         return render_template('oscar/usermanage/userchangepass.html')
   else:
      return render_template('oscar/usermanage/userchangepass.html')
