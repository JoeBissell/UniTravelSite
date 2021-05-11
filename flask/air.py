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

# DATABASE CONNECTION
def getConnection():    
    try:
        conn = mysql.connector.connect(host='localhost',                              
                              user='root',
                              password='Doctorwho123?£',
                              database='airtravel')  
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('User name or Password is not working')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist')
        else:
            print(err)                        
    else:  #will execute if there is no exception raised in try block
        return conn
 
# HOMEPAGE
@app.route('/airtravelhome')         
def airtravelhome():  
   if 'username' in session:
      username = session['username']
      return render_template('/hollie/airTravelwelcome.html', username=username)
   else:
      return render_template('/hollie/airTravelwelcome.html')

# LOGIN REQUIRED
def requiredLogin(f):
   @wraps(f)
   def wrap(*args, **kwargs):
      if 'logged_in' in session:
         return f(*args, **kwargs)
      else:
         print("Login is required.")
      return render_template("hollie/airTravellogin.html", error="You are required to login first!")
   return wrap

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
            conn = getConnection()
            if conn != None:
               if conn.is_connected():
                  print('Connected to DB.')
                  dbcursor = conn.cursor()
                  dbcursor.execute("SELECT password_hash, usertype, airuserid FROM airusers WHERE username = %s;", (username,))
                  data = dbcursor.fetchone()
                  if dbcursor.rowcount < 1:
                     error = " The Username or Password entered is incorrect"
                     return render_template("hollie/airTravelsignup.html", error=error)
                  else:
                     if sha256_crypt.verify(request.form['password'], str(data[0])):
                        session['logged_in'] = True
                        session['username'] = request.form['username']
                        session['usertype'] = str(data[1])
                        session['airuserid'] = str(data[2])
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

# CHECKING LOGIN / ALREADY LOGGED IN
def airTravelloginCheck(f):
    @wraps(f)
    def wrap(*args, **kwargs):
      if ('logged_in' not in session):
         return f(*args, **kwargs)
      else:
         return render_template('hollie/airTravelwelcome.html' , error= 'Already logged in')
    return wrap

# LOG OUT OF ACCOUNT
@app.route('/logoutairtravel')
def logoutairtravel():
   session.clear()
   print("Logged out.")
   gc.collect()
   return render_template('/hollie/airTravelwelcome.html')

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
            conn = getConnection()
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
                     return render_template("hollie/airTravelsignup.html")
               else:
                  error = "Connection error."
                  print("Wrong!")
                  return render_template("hollie/airTravelreg.html", error=error)
            else: 
               error = "Connection error."
               print("Nope!")
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

# PROCESS FOR USERS
# BOOKING PROCESS
@app.route('/airtravelbooking', methods=['POST', 'GET'])
@requiredLogin
def airtravelbooking():
      conn = getConnection()
      if conn != None:           
         print('Connected to DB.')                          
         dbcursor = conn.cursor()             
         dbcursor.execute('SELECT DISTINCT leaving FROM airroutes;')   
         print('SELECT executed.')             
         rows = dbcursor.fetchall()                                    
         dbcursor.close()              
         conn.close() 
         airplace = []
         for place in rows:
            place = str(place).strip("(")
            place = str(place).strip(")")
            place = str(place).strip(",")
            place = str(place).strip("'")
            airplace.append(place)
         return render_template('hollie/airTravelbooking.html', leavinglist=airplace)
      else:
         print('Connection error.')
         return 'Connection error.'

## BOOKINGS FETCH ARRIVALS
@app.route ('/airtravelarrival/', methods = ['POST', 'GET'])
@requiredLogin
def ajax_returnairtravel():   
	print('Fetching arrivals.') 
	if request.method == 'GET':
		arrival = request.args.get('q')
		conn = getConnection()
		if conn != None:          
			print('Connected to DB.')                          
			dbcursor = conn.cursor()             
			dbcursor.execute('SELECT DISTINCT arrival FROM airroutes WHERE leaving = %s;', (arrival,))   
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
@app.route ('/airtravelbookingselect/', methods = ['POST', 'GET'])
@requiredLogin
def airtravelbooking_select():
   if request.method == 'POST':
      print('Booking initiated.')
      leavingcity = request.form['departureslist']
      arrivalcity = request.form['arrivalslist']
      outdate = request.form['outdate']
      returndate = request.form['returndate']
      adultseats = request.form['adultseats']
      childseats = request.form['childseats']
      lookupdata = [leavingcity, arrivalcity, outdate, returndate, adultseats, childseats]
      conn = getConnection()
      if conn != None:
         print('Connected to DB.')
         dbcursor = conn.cursor()
         dbcursor.execute('SELECT * FROM airroutes WHERE leaving = %s AND arrival = %s', (leavingcity, arrivalcity))
         print('SELECT executed.')
         rows = dbcursor.fetchall()
         datarows=[]
         for row in rows:
            data = list(row)
            print('Working')
            print(row[5])
            print(data) 
            print(datarows)                 
            fare = (float(row[6]) * float(adultseats)) + (float(row[6]) * 0.5 * float(childseats))
            print(fare)
            data.append(fare)
            print(data)
            datarows.append(data)	
         dbcursor.close()
         conn.close()
         return render_template('hollie/airTravelstartbooking.html', resultset=datarows, lookupdata=lookupdata)
      else:
         print('Connection error.')
         return redirect(url_for('index'))

## BOOKING CONFIRM
@app.route('/airtravelbookingconfirm/', methods=['POST', 'GET'])
@requiredLogin
def airtravelbooking_confirm():
   if request.method == 'POST':
      print('Booking initiated.')
      airid = request.form['bookingchoice']
      departcity = request.form['deptcity']
      arrivalcity = request.form['arrivcity']
      leavedate = request.form['outdate']
      returndate = request.form['returndate']
      childSeats = request.form['childseats']
      adultSeats = request.form['adultseats']
      totalfare = request.form['totalfare']
      cardnumber = request.form['cardnumber']
      airuserid = session['airuserid']
      username = session['username']
      totalseats = int(adultSeats) + int(childSeats)
      bookingdata = [airid, departcity, arrivalcity, leavedate, returndate, childSeats, adultSeats, totalfare, airuserid]
      print(bookingdata)
      conn = getConnection()
      if conn != None:
         print ('Connected to DB.')
         dbcursor = conn.cursor()
         dbcursor.execute('INSERT INTO airtravelbooking (leavingdate, airid, numseats, totalfare, airuserid) VALUES \
            (%s, %s, %s, %s, %s);', (leavedate, airid, totalseats, totalfare, airuserid))
         print('INSERT executed.')
         conn.commit()
         dbcursor.execute('SELECT LAST_INSERT_ID();')
         rows = dbcursor.fetchone()
         bookingid = rows[0]
         bookingdata.append(bookingid)
         dbcursor.execute('SELECT * FROM airroutes WHERE airid = %s', (airid,))
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
         return render_template('hollie/airTravelbookcon.html', username=username, resultset=bookingdata, cardnumber=cardnumber, airuserid=airuserid)
   else:
      print('Connection error.')
      error = 'Connection error.'
      return render_template('airTravelwelcome.html', error=error)

@app.route ('/varDump/', methods = ['POST', 'GET'])
def varDump():
	if request.method == 'POST':
		result = request.form
		output = "<H2>Booking Confirmed: </H2></br>"
		output += "Number of Data Fields : " + str(len(result))
		for key in list(result.keys()):
			output = output + " </br> " + key + " : " + result.get(key)
		return output
	else:
		result = request.args
		output = "<H2>Booking Confirmed: </H2></br>"
		output += "Number of Data Fields : " + str(len(result))
		for key in list(result.keys()):
			output = output + " </br> " + key + " : " + result.get(key)
		return output  

# USER FEATURES
# USER MANAGEMENT PAGE
@app.route('/airtravelusermanag')         
def airtravelusermanag():  
   if 'username' in session:
      username = session['username']
      return render_template('/hollie/airTraveluserman.html', username=username)
   else:
      return render_template('/hollie/airTraveluserman.html')
# VIEW BOOKING
@app.route('/air_viewbookings', methods=['GET', 'POST'])
@requiredLogin
def air_viewbookings():
   conn = getConnection()
   if conn != None:
      if conn.is_connected():
         airuserid = session['airuserid']
         username = session['username']
         print('Connected to DB.')
         dbcursor = conn.cursor()
         dbcursor.execute('SELECT * FROM airtravelbooking WHERE airuserid = %s;', (airuserid,))
         print('SELECT bookings executed.')
         bookingrows = dbcursor.fetchall()
         dbcursor.close()
         conn.close()
         if not bookingrows:
            error = 'No bookings'
            print(error)
            return render_template('hollie/airTraveluserman.html', error=error)
         else:
            print(bookingrows)
            return render_template('hollie/airTravelviewbook.html', bookingresult=bookingrows, airuserid=airuserid, username=username)
      else:
         error = "Connection error."
         print(error)
         return render_template("hollie/airTraveluserman.html", error=error)
   else:
         error = "Connection error."
         print(error)
         return render_template("hollie/airTraveluserman.html", error=error)
# DELETE BOOKING
@app.route('/air_cancelbooking', methods=['POST', 'GET'])
@requiredLogin
def air_cancelbooking():
   if request.method == 'GET':
      bookingid = request.args.get('deletebooking')
      if bookingid != None:
         conn=getConnection()
         if conn != None:
            if conn.is_connected():
               print('Connected to DB.')
               dbcursor = conn.cursor()
               sql_statement = 'DELETE FROM airtravelbooking WHERE airbookingid = %s'
               args = (bookingid,)
               dbcursor.execute(sql_statement, args)
               print('DELETE executed.')
               conn.commit()
               dbcursor.close()
               conn.close()
               msg = 'booking has been canceled'
               return render_template('hollie/airTraveluserman.html', msg=msg)
            else:
               print('Connection error.')
         else:
            error = "Connection error."
            return render_template("hollie/airTraveluserman.html", error=error)
      else:
         error = "no bookings available"
         return render_template('hollie/airTraveluserman.html', error=error)
# CHANGING THEIR ROUTE

# ADMIN FEATURES
# ADMIN LOG IN REQUIRED
def required_admin(f):
   @wraps(f)
   def wrap(*args, **kwargs):
      if ('logged_in' in session) and (session['usertype'] == 'admin'):
         return f(*args, **kwargs)
      else:
         print("Admin login required.")
         abort(401)
   return wrap

# ADDING A ROUTE 

# DELETING A ROUTE

# AMENDING A ROUTE