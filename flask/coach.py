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


def get_connection():
   conn = mysql.connector.connect(host='localhost',
                                  user='suleima2abbara',
                                  password='Suleima2abbarA14+$++',
                                  database='suleima2abbara_prj')
   return conn

## route to home page
@app.route('/coachhome')         
def coachhome():    
   username = session['username']   
   return render_template('/suleima/coach.html', username=username)

@app.route("/coach", methods=['POST', 'GET']) 
def coach():
   username = session['username']   
   return render_template('/suleima/coach.html', username=username)




@app.route("/regsuccess", methods=['POST', 'GET']) 
def regsuccess():
    username = session['username']
    return render_template('/suleima/regsuccess.html')


@app.route('/coachreg', methods=['POST', 'GET'])
def coachreg():
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

## COACH LOG IN
@app.route('/coachlogin', methods=["GET", "POST"])
def coachlogin():
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
                           return render_template("suleima/admin.html", username=username, data='user specific data', usertype=session['usertype'], userid=session['userid'])
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

## LOG OUT
@app.route('/coachlogout')
def coachlogout():
   session.clear()
   print("Logged out.")
   gc.collect()
   return render_template('/suleima/coachhome.html')

@app.route("/loginsuccess", methods=['POST', 'GET']) 
def loginsuccess():
    username=request.form['username']
    return render_template('/suleima/loginsuccess.html')

@app.route("/coachbook", methods=['POST', 'GET']) 
def coachbook():
   username = session['username']
   conn = get_connection()
   print('MySQL Connection is established')                          
   dbcursor = conn.cursor()    #Creating cursor object            
   dbcursor.execute('SELECT DISTINCT deptCity FROM coachroutes3;')   
   print('SELECT statement executed successfully.')             
   rows = dbcursor.fetchall()                                    
   dbcursor.close()              
   conn.close() #Connection must be 
   cities = []
   for city in rows:
      city = str(city).strip("(")
      city = str(city).strip(")")
      city = str(city).strip(",")
      city = str(city).strip("'")
      cities.append(city)
   return render_template('/suleima/coachbook.html', departurelist=cities)

@app.route ('/arrivalcoach/', methods = ['POST', 'GET'])
def ajax_returncoach():   
	print('/arrivalcity') 

	if request.method == 'GET':
		deptcity = request.args.get('q')
		conn = get_connection()
		if conn != None:    #Checking if connection is None         
			print('MySQL Connection is established')                          
			dbcursor = conn.cursor()    #Creating cursor object            
			dbcursor.execute('SELECT DISTINCT arrivCity FROM coachroutes3 WHERE deptCity = %s;', (deptcity,))   
			print('SELECT arrival statement executed successfully.')             
			rows = dbcursor.fetchall()
			total = dbcursor.rowcount                                    
			dbcursor.close()              
			conn.close() #Connection must be closed			
			return jsonify(returncities=rows, size=total)
		else:
			print('DB connection Error')
			return jsonify(returncities='DB Connection Error')

@app.route ('/select-coach/', methods = ['POST', 'GET'])
def select_coach():
	if request.method == 'POST':
		print('Select booking initiated')
		departcity = request.form['departureslist']
		arrivalcity = request.form['arrivalslist']
		outdate = request.form['outdate']
		returndate = request.form['returndate']
		adultseats = request.form['adultseats']
		childseats = request.form['childseats']
		lookupdata = [departcity, arrivalcity, outdate, returndate, adultseats, childseats]
		#print(lookupdata)
		conn = get_connection()
		if conn != None:    #Checking if connection is None         
			print('MySQL Connection is established')                          
			dbcursor = conn.cursor()    #Creating cursor object            
			dbcursor.execute('SELECT * FROM coachroutes3 WHERE deptCity = %s AND arrivCity = %s;', (departcity, arrivalcity))   
		#	print('SELECT statement executed successfully.')             
			rows = dbcursor.fetchall()
			datarows=[]			
			for row in rows:
				data = list(row)                    
				fare = (float(row[5]) * float(adultseats)) + (float(row[5]) * 0.5 * float(childseats))
				#print(fare)
				data.append(fare)
				#print(data)
				datarows.append(data)			
			dbcursor.close()              
			conn.close() #Connection must be closed
			#print(datarows)
			#print(len(datarows))			
			return render_template('/suleima/c_bookstart.html', resultset=datarows, lookupdata=lookupdata)
		else:
			print('DB connection Error')
			return redirect(url_for('index'))