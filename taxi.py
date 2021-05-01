import mysql.connector
from flask import Flask, render_template, request, session, redirect, url_for, escape, abort, jsonify, redirect
from passlib.hash import sha256_crypt
import hashlib
import gc
from functools import wraps
from datetime import datetime

app = Flask(__name__)   
app.secret_key = 'verysecretkey'

## create connection to DB
def get_connection():
   conn = mysql.connector.connect(host='localhost',
                                  user='root',
                                  password='password',
                                  database='travelsite')
   return conn

## route to index page
@app.route('/oscarindex')         
def oscarindex():  
   if 'username' in session:
      username = session['username']
      return render_template('/oscar/index.html', username=username)          
   print ('Hello')      
   return render_template('/oscar/index.html')


## LOGIN/LOGOUT FUNCTIONS ##
## already logged in
def check_login(f):
   @wraps(f)
   def wrap(*args, **kwargs):
      if ('logged_in' not in session):
         return f(*args, **kwargs)
      else: 
         print('already logged in')
         return render_template('oscar/index.html', error= 'already logged in')
   return wrap

## login route
@app.route('/oscarlogin', methods=["GET", "POST"])
@check_login
def oscarlogin():
   form={}
   error = ''
   try:
      if request.method == "POST":
         username = request.form['username']
         password = request.form['password']
         print('login start 1.1')

         if username !=None and password != None:
            conn = get_connection()
            if conn != None:
               if conn.is_connected():
                  print('SQL connection established')
                  dbcursor = conn.cursor()
                  dbcursor.execute("SELECT password_hash, usertype FROM taxiusers where username = %s;", (username,))
                  data = dbcursor.fetchone()
                  if dbcursor.rowcount < 1:
                     error = "username/password incorrect"
                     return render_template("oscar/login.html", error=error)
                  else:
                     if sha256_crypt.verify(request.form['password'], str(data[0])):
                        session['logged_in'] = True
                        session['username'] = request.form['username']
                        session['usertype'] = str(data[1])
                        print("you are logged in")
                        if session['usertype'] == 'admin':
                           return render_template("oscar/admin/admin.html", username=username, data='user specific data', usertype=session['usertype'])
                        else: 
                           return render_template("oscar/login-success.html", username=username, data='user specific data', usertype=session['usertype'])
                     else:
                        error = "invalid credentials1"
               gc.collect()
               print('login start 1.10')
               return render_template("oscar/login.html", form=form, error=error)
   except Exception as e:
      error = str(e) + "invalid credentials2"
      render_template("oscar/login.html", form=form, error=error)
   return render_template("oscar/login.html", form=form, error=error)

## logout route
@app.route('/oscarlogout')
def oscarlogout():
   session.clear()
   print("logged out")
   gc.collect()
   return render_template('oscar/index.html')

## login required
def login_req(f):
   @wraps(f)
   def wrap(*args, **kwargs):
      if 'logged_in' in session:
         return f(*args, **kwargs)
      else:
         print("you must login")
      return render_template("login.html", error="Please login first")
   return wrap

## admin login required
def admin_req(f):
   @wraps(f)
   def wrap(*args, **kwargs):
      if ('logged_in' in session) and (session['usertype'] == 'admin'):
         return f(*args, **kwargs)
      else:
         print("log in as admin")
         abort(401)
   return wrap
## END OF LOGIN/LOGOUT FUNCTIONS ##

## basic lookup of taxi service routes
@app.route('/oscarlookup')
def oscarlookup():
   conn = get_connection()
   if conn != None:
      if conn.is_connected():
         print('SQL connection established')
         dbcursor = conn.cursor()
         SQL_statement = 'SELECT DISTINCT leaving FROM taxiroutes;'
         dbcursor.execute(SQL_statement)
         print('SELECT statement executed.')
         rows = dbcursor.fetchall()
         dbcursor.close()
         conn.close()
         return render_template('/oscar/lookup.html', resultset=rows)
      else:
         print('db connect error')
         return ('db connect error')
   else: 
      print('db connect error')
      return ('db connect error')

## get results from taxi lookup page
@app.route('/oscar_show_route', methods=['POST','GET'])
def oscar_show_route():
   if request.method =='GET':
      leaving = request.args.get('leaving')
      if leaving != None:
         conn = get_connection()
         if conn != None:
            if conn.is_connected():
               print ('sql connection established')
               dbcursor = conn.cursor()
               SQL_statement = 'SELECT * FROM taxiroutes WHERE leaving = %s'
               args = (leaving,)
               dbcursor.execute(SQL_statement, args)
               print('SELECT statement executed')
               rows = dbcursor.fetchall()
               dbcursor.close()
               conn.close()
               return render_template('oscar/lookup-results.html', resultset=rows)
            else:
               print('db connect error')
               return 'db connect error'
         else:
            print('db connect error')
            return 'db connect error'
      else: 
         print('invalid route')
         return render_template('oscar/index.html')

## admin page
@app.route('/admin')
@admin_req
def admin():
   print ('Hello')
   return render_template('admin.html')

## admin insert new route
@app.route('/oscar_admininsert')
@admin_req
def oscar_admininsert():
   print ('Hello')
   return render_template('oscar/admin/admininsert.html')

## ADMIN FUNCTIONS ##
## admin show all records
@app.route('/oscar_adminroutes')
@admin_req
def oscar_adminroutes():
   print ('Hello')
   conn = get_connection()
   if conn != None:
      if conn.is_connected():
         print('conn established')
         dbcursor = conn.cursor()
         dbcursor.execute('SELECT * FROM taxiroutes;')
         print('select executed')
         rows = dbcursor.fetchall()
         dbcursor.close()
         conn.close()
         return render_template('oscar/admin/adminroutes.html', resultset=rows)
      else:
         print('connect error')
         return('connect error')
   else:
      print ('connect error')
      return 'connect error'

##insert route
@app.route('/oscaradmininsert', methods=['POST', 'GET'])
@admin_req
def oscaradmininsert():
   msg=""
   print('adding route')
   if request.method == 'POST':
      try:
         leaving = request.form['leaving']
         leavingtime = request.form['leavingtime']
         arrival = request.form['arrival']
         arrivaltime = request.form['arrivaltime']
         miles = request.form['miles']
         print('try')
         msg = leaving + leavingtime + arrival + arrivaltime + miles
         print('msg')
         conn = get_connection()
         if conn.is_connected():
            cursor = conn.cursor()
            sql_statement = "INSERT INTO travelsite.taxiroutes (leaving, leavingtime, arrival, arrivaltime, miles) VALUES (%s, %s, %s, %s, %s)"
            print(cursor)
            args = (leaving, leavingtime, arrival, arrivaltime, miles)
            cursor.execute(sql_statement, args)
            conn.commit()
            cursor.close()
            msg = "Record added"
         print(msg)
      except:
         print('except')
         conn.rollback()
         msg += "error in insert op"
         print(msg)
      finally:
         print('finally')
         return render_template('oscar/admin/admin.html', msg= msg)
   else:
      print('not post')
      return 'not post'

##remove route
@app.route('/oscaradminremoveroute', methods=['POST', 'GET'])
@admin_req
def oscaradminremoveroute():
   if request.method == 'GET':
      routeid = request.args.get('removeroute')
      print('route id= =', routeid)
      if routeid != None:
         conn=get_connection()
         if conn != None:
            if conn.is_connected():
               print('connected')
               dbcursor = conn.cursor()
               sql_statement = 'DELETE FROM taxiroutes WHERE id = %s'
               args = (routeid,)
               dbcursor.execute(sql_statement, args)
               print('command executed')
               conn.commit()
               dbcursor.close()
               conn.close()
               msg = 'Record removed'
               return render_template('oscar/admin/admin.html', msg=msg)
            else:
               print('connect error')
         else:
            print('db connect error')
            return 'db connect error'
      else:
         print('invalid tutor id')
         return render_template('oscar/admin/admin.html')

##change time of route
##add booking
##remove booking

## registration page
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
                  print ('MySQL connection established')
                  dbcursor = conn.cursor()
                  password = sha256_crypt.hash((str(password)))
                  Verify_Query = "SELECT * FROM taxiusers WHERE username = %s;"
                  dbcursor.execute(Verify_Query,(username,))
                  rows = dbcursor.fetchall()
                  if dbcursor.rowcount > 0:
                     print ('username already taken')
                     error = "username already taken"
                     return render_template("oscar/register.html", error=error)
                  else:
                     dbcursor.execute("INSERT INTO taxiusers (username, password_hash,  email) VALUES (%s, %s, %s)", (username, password, email))
                     conn.commit()
                  print("registered")
                  dbcursor.close()
                  conn.close()
                  gc.collect()
                  return render_template("oscar/success.html")
            else:
               print('Connection error')
               return ' DB connection error '
         else: 
            print ('Connection error')
            return ' DB connection error '
      else:
         print('empty parameters')
         return render_template("oscar/register.html", error=error)
   except Exception as e:
      return render_template("oscar/register.html", error=e)
   return render_template("oscar/register.html", error=error)

##BOOKINGS
@app.route('/oscarbookings')
def oscarbookings():
	conn = get_connection()
	if conn != None:    #Checking if connection is None         
		print('MySQL Connection is established')                          
		dbcursor = conn.cursor()    #Creating cursor object            
		dbcursor.execute('SELECT DISTINCT leaving FROM taxiroutes;')   
		#print('SELECT statement executed successfully.')             
		rows = dbcursor.fetchall()                                    
		dbcursor.close()              
		conn.close() #Connection must be 
		leavingcity = []
		for leaving in rows:
			leaving = str(leaving).strip("(")
			leaving = str(leaving).strip(")")
			leaving = str(leaving).strip(",")
			leaving = str(leaving).strip("'")
			leavingcity.append(leaving)
		return render_template('oscar/bookings/bookings.html', leavinglist=leavingcity)
	else:
		print('DB connection Error')
		return 'DB Connection Error'
	
@app.route ('/oscarreturnarrival/', methods = ['POST', 'GET'])
def ajax_returnarrival():   
	print('/oscarreturnarrival') 

	if request.method == 'GET':
		arrival = request.args.get('q')
		conn = get_connection()
		if conn != None:    #Checking if connection is None         
			print('MySQL Connection is established')                          
			dbcursor = conn.cursor()    #Creating cursor object            
			dbcursor.execute('SELECT DISTINCT arrival FROM taxiroutes WHERE leaving = %s;', (arrival,))   
			#print('SELECT statement executed successfully.')             
			rows = dbcursor.fetchall()
			total = dbcursor.rowcount                                    
			dbcursor.close()              
			conn.close() #Connection must be closed			
			return jsonify(returncities=rows, size=total)
		else:
			print('DB connection Error')
			return jsonify(returncities='DB Connection Error')