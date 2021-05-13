import mysql.connector
from flask import Flask, render_template, request, session, redirect, url_for, escape, abort, jsonify
from passlib.hash import sha256_crypt
import hashlib
import gc
from functools import wraps
# from flask_wtf import FlaskForm  -- Commented this out as not a module name
#from wtforms import StringField, PasswordField, SubmitField, BooleanField
#from wtforms.validators import DataRequired, Length, Email, EqualTo

app = Flask(__name__) 
app.secret_key = 'brad'

#Connect to database
def get_connection():
   conn = mysql.connector.connect(host='localhost',
                                  user='bradley2verrinder',
                                  password='Bradley2verrindeR17+$++',
                                  database='bradley2verrinder_prj')
   return conn

#Home page
@app.route('/')
def Trainhomes():
   return render_template('/brad/Trainhome.html') 

@app.route('/Trainhome')        
def Trainhome():
   if 'username' in session:
      username = session['username'] 
      return render_template('/brad/Trainlogin.html')

@app.route("/Train", methods=['POST', 'GET']) 
def Train():
    username = session['username'] 
    return render_template('/brad/Trainlogin.html', username=username)


#Display registration success message 
@app.route("/regsuccess", methods=['POST', 'GET']) 
def regsuccess():
    username = request.form['username']
    return render_template('/brad/regsuccess.html')

#Registration feature
@app.route('/Trainreg', methods=['POST', 'GET'])
def Trainreg():
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
                  #password = sha256_crypt.hash((str(password))) - I HAD PROBLEMS WITH MY INSERT STATEMENT MEANING I HAD TO COMMENT OUT THE PASSWORD HASHING
                  Verify_Query = "SELECT * FROM trainusers WHERE username = %s;"
                  dbcursor.execute(Verify_Query,(username,))
                  print ("SELECT executed.")
                  rows = dbcursor.fetchall()
                  if dbcursor.rowcount > 0:
                     print ('Username taken.')
                     error = "Username already taken."
                     return render_template("/brad/Trainreg.html", error=error)
                  else:
                     #due to an error when registering these values will be the only values that allow you to login despite your input during registration, i have spoken to Zaheer about this and this is what he instructed me to do.
                     #dbcursor.execute("INSERT INTO trainusers (username, password_hash, email) VALUES (%s, %s, %s)", (username, password, email))
                     dbcursor.execute("INSERT INTO trainusers (username, password_hash, email) VALUES ('user', 'password', 'user@123.com')")
                     conn.commit()
                     print("INSERT executed. Registration complete.")
                     dbcursor.close()
                     conn.close()
                     gc.collect()
                     return render_template("/brad/regsuccess.html")
               else:
                  error = "Connection error."
                  return render_template("/brad/Trainreg.html", error=error)
            else: 
               error = "Connection error."
               return render_template("/brad/Trainreg.html", error=error)
         else:
            print('Empty parameters.')
            return render_template("/brad/Trainreg.html", error=error)
   except Exception as e:
      return render_template("/brad/Trainreg.html", error=e)
   return render_template("/brad/Trainreg.html", error=error)

#Login Feature
@app.route('/Trainlogin', methods=["GET", "POST"])
def Trainlogin():
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
                  dbcursor.execute("SELECT password_hash, accountType, userId FROM trainusers WHERE username = %s;", (username,))
                  data = dbcursor.fetchone()
                  if dbcursor.rowcount < 1:
                     error = "Username or password incorrect"
                     return render_template("/brad/Trainlogin.html", error=error)
                  else:
                     if (request.form['password'], str(data[0])):
                        session['logged_in'] = True
                        session['username'] = request.form['username']
                        session['accountType'] = str(data[1])
                        session['userId'] = str(data[2])
                        print("Already logged in.")
                        return render_template("/brad/loginsuccess.html", username=username, data='user specific data', accountType=session['accountType'], userId=session['userId'])
                     else:
                        error = "Invalid login 1."
               gc.collect()
               return render_template("/brad/Trainlogin.html", form=form, error=error)
   except Exception as e:
      error = str(e) + "Invalid login 2."
      render_template("/brad/Trainlogin.html", form=form, error=error)
   return render_template("/brad/Trainlogin.html", form=form, error=error)

#Required login before booking
def requiredLogin(f):
   @wraps(f)
   def wrap(*args, **kwargs):
      if 'logged_in' in session:
         return f(*args, **kwargs)
      else:
         print("Login is required.")
      return render_template("/brad/Trainlogin.html", error="You are required to login first!")
   return wrap


#Logout feature
@app.route('/Trainlogout',)
def Trainlogout():
   session.clear()
   print("Logged out.")
   gc.collect()
   return render_template('/brad/Trainlogin.html')

#Display login success message
@app.route("/loginsuccess", methods=['POST', 'GET']) 
def loginsuccess():
    username=request.form['username']
    return render_template('/brad/loginsuccess.html')

#Booking process
@app.route('/Trainbooking', methods=['POST', 'GET'])
@requiredLogin
def Trainbooking():
      conn = get_connection()
      if conn != None:           
         print('Connected to DB.')                          
         dbcursor = conn.cursor()             
         dbcursor.execute('SELECT DISTINCT departureCity FROM journeys;')   
         print('SELECT executed.')             
         rows = dbcursor.fetchall()                                    
         dbcursor.close()              
         conn.close() 
         Trainplace = []
         for place in rows:
            place = str(place).strip("(")
            place = str(place).strip(")")
            place = str(place).strip(",")
            place = str(place).strip("'")
            Trainplace.append(place)
         return render_template('/brad/Trainbooking.html', leavinglist=Trainplace)
      else:
         print('Connection error.')
         return 'Connection error.'

#Fetch arrivals
@app.route ('/Trainarrival/', methods = ['POST', 'GET'])
@requiredLogin
def ajax_returntraintravel():   
	print('Fetching arrivals.') 
	if request.method == 'GET':
		arrival = request.args.get('q')
		conn = get_connection()
		if conn != None:          
			print('Connected to DB.')                          
			dbcursor = conn.cursor()             
			dbcursor.execute('SELECT DISTINCT destination FROM journeys WHERE departureCity = %s;', (arrival,))   
			print('SELECT executed.')          
			rows = dbcursor.fetchall()
			total = dbcursor.rowcount                                    
			dbcursor.close()              
			conn.close() 		
			return jsonify(returncities=rows, size=total)
		else:
			print('Connection error.')
			return jsonify(returncities='Connection error.')

#Select booking
@app.route ('/Trainselectbooking/', methods = ['POST', 'GET'])
@requiredLogin
def Trainselect_booking():
   if request.method == 'POST':
      print('Booking initiated.')
      leavingcity = request.form['departureslist']
      arrivalcity = request.form['arrivalslist']
      outdate = request.form['outdate']
      returndate = request.form['returndate']
      adultseats = request.form['adultseats']
      childseats = request.form['childseats']
      lookupdata = [leavingcity, arrivalcity, outdate, returndate, adultseats, childseats]
      conn = get_connection()
      if conn != None:
         print('Connected to DB.')
         dbcursor = conn.cursor()
         dbcursor.execute('SELECT * FROM journeys WHERE departureCity = %s AND destination = %s', (leavingcity, arrivalcity))
         print('SELECT executed.')
         rows = dbcursor.fetchall()
         datarows=[]
         for row in rows:
            data = list(row)
            print('Working')
            print(row[5])
            print(data) 
            print(datarows)                 
            fare = (float(row[5]) * float(adultseats)) + (float(row[5]) * 0.5 * float(childseats))
            print(fare)
            data.append(fare)
            print(data)
            datarows.append(data)	
         dbcursor.close()
         conn.close()
         return render_template('/brad/Trainbookingstart.html', resultset=datarows, lookupdata=lookupdata)
      else:
         print('Connection error.')
         return redirect(url_for('index'))

#Confirm booking
@app.route('/Trainconfirmbooking/', methods=['POST', 'GET'])
@requiredLogin
def Trainconfirm_booking():
   if request.method == 'POST':
      print('Booking initiated.')
      idJourneys = request.form['bookingchoice']
      departcity = request.form['deptcity']
      arrivalcity = request.form['arrivcity']
      leavedate = request.form['outdate']
      returndate = request.form['returndate']
      childSeats = request.form['childseats']
      adultSeats = request.form['adultseats']
      totalfare = request.form['totalfare']
      cardnumber = request.form['cardnumber']
      userId = session['userId']
      username = session['username']
      totalseats = int(adultSeats) + int(childSeats)
      bookingdata = [idJourneys, departcity, arrivalcity, leavedate, returndate, childSeats, adultSeats, totalfare, userId]
      print(bookingdata)
      conn = get_connection()
      if conn != None:
         print ('Connected to DB.')
         dbcursor = conn.cursor()
         dbcursor.execute('INSERT INTO reservation (departureDate, destinationDate, seatNum, ticketFare, idJourneys, userId) VALUES \
            (%s, %s, %s, %s, %s, %s);', (leavedate, returndate, totalseats, totalfare, idJourneys, userId))
         print('INSERT executed.')
         conn.commit()
         dbcursor.execute('SELECT LAST_INSERT_ID();')
         rows = dbcursor.fetchone()
         bookingid = rows[0]
         bookingdata.append(bookingid)
         dbcursor.execute('SELECT * FROM reservation WHERE idReserve = %s', (idJourneys,))
         print(bookingdata)
         rows = dbcursor.fetchall()
         #deptTime = rows[0][3]  #These parts are commented as I chose not to display the time
         #arrivTime = rows[0][4]   
         print(bookingdata)
         #bookingdata.append(deptTime)
         #bookingdata.append(arrivTime)
         cardnumber = cardnumber[-4:-1]
         print(cardnumber)
         dbcursor.execute
         dbcursor.close()
         conn.close()
         return render_template('/brad/Trainbookconfirm.html', username=username, resultset=bookingdata, cardnumber=cardnumber, userId=userId)
   else:
      print('Connection error.')
      error = 'Connection error.'
      return render_template('/brad/Trainhome.html', error=error)

#Booking receipt
@app.route ('/varDump/', methods = ['POST', 'GET'])
def varDump():
	if request.method == 'POST':
		result = request.form
		output = "<H2>Confirmed Booking: </H2></br>"
		output += "Number of Data Fields : " + str(len(result))
		for key in list(result.keys()):
			output = output + " </br> " + key + " : " + result.get(key)
		return output
	else:
		result = request.args
		output = "<H2>Confirmed Booking: </H2></br>"
		output += "Number of Data Fields : " + str(len(result))
		for key in list(result.keys()):
			output = output + " </br> " + key + " : " + result.get(key)
		return output  


#Cancel Booking
@app.route('/Train_cancelbooking', methods=['POST', 'GET'])
@requiredLogin
def Train_cancelbooking():
   if request.method == 'GET':
      bookingid = request.args.get('deletebooking')
      if bookingid != None:
         conn=get_connection()
         if conn != None:
            if conn.is_connected():
               print('Connected to DB.')
               dbcursor = conn.cursor()
               sql_statement = 'DELETE FROM reservation WHERE idReserve = %s'
               args = (bookingid,)
               dbcursor.execute(sql_statement, args)
               print('DELETE executed.')
               conn.commit()
               dbcursor.close()
               conn.close()
               msg = 'Congratulations! Your booking has been cancelled'
               return render_template('/brad/Trainhome.html', msg=msg)
            else:
               print('Connection error.')
         else:
            error = "Connection error."
            return render_template("/brad/Trainhome.html", error=error)
      else:
         error = "no bookings available"
         return render_template('/brad/Trainhome.html', error=error)


# view previous bookings
@app.route('/Trainviewbook', methods=['GET', 'POST'])
@requiredLogin
def Trainviewbook():
   conn = get_connection()
   if conn != None:
      if conn.is_connected():
         userId = session['userId']
         username = session['username']
         print('database connection successful')
         dbcursor = conn.cursor()
         dbcursor.execute('SELECT * FROM reservation WHERE userId = %s;', (userId,))
         print('SELECT bookings executed.')
         bookingrows = dbcursor.fetchall()
         dbcursor.close()
         conn.close()
         if not bookingrows:
            error = 'there are no bookings available'
            print(error)
            return render_template('/brad/Trainhome.html', error=error)
         else:
            print(bookingrows)
            return render_template('/brad/Trainviewbook.html', bookingresult=bookingrows, userId=userId, username=username)
      else:
         error = "Connection error."
         print(error)
         return render_template("/brad/Trainhome.html", error=error)
   else:
         error = "Connection error."
         print(error)
         return render_template("/brad/Trainhome.html", error=error)


app.run(debug = True, port = 5050)

