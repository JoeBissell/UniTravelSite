from __main__ import app, get_connection
from flask import Flask, render_template, request, session, redirect, url_for, escape, abort, jsonify, redirect
from passlib.hash import sha256_crypt
import mysql.connector

@app.route("/joe")
def joe():
    conn = get_connection()
    if conn != None:
        dbcursor = conn.cursor()
        query = 'SELECT manufacturer, brand, numberOfSeats, costPerDay, type FROM carhire'
        dbcursor.execute(query)
        results = dbcursor.fetchall()
        dbcursor.close

        return render_template("joe/index.html", carDetails = results)

@app.route("/viewbookings")
def viewbookings():
    return render_template("joe/pages/viewbookings.html")

@app.route("/booktickets")
def booktickets():
    conn = get_connection()
    if conn != None:
        dbcursor = conn.cursor()
        query = 'SELECT carID, manufacturer, brand, numberOfSeats, costPerDay, type FROM carhire'
        dbcursor.execute(query)
        results = dbcursor.fetchall()
        dbcursor.close

        return render_template("joe/pages/makebookings.html", carDetails = results)
    return render_template("joe/pages/makebookings.html", msg = "not_logged_in")

@app.route("/bookcar")
def bookcar():
    conn = get_connection()
    dbcursor = conn.cursor()
    car_id =request.args.get('carid')
    user_id = session['userid']
    query = 'UPDATE carhire SET bookedBy = %s WHERE carid = %s;'
    dbcursor.execute(query, (user_id, car_id))
    conn.commit()

    return 'done'

@app.route("/cancelbookings")
def cancelbookings():
    return render_template("joe/pages/cancelbookings.html")

@app.route("/carhireloginregister")
def carhireloginregister():
    return render_template("joe/pages/login.html")

@app.route("/carhireregister", methods=['POST', 'GET'])
def carhireregister():
    if request.method == "POST":
        email = request.form["register-email"]
        username = request.form["register-username"]
        password = request.form["register-password"]
        conn = get_connection()
        if conn != None:
            dbcursor = conn.cursor()
            # Check if username is already in use
            query = "SELECT * FROM carhireusers WHERE username = %s;"
            dbcursor.execute(query,[username])
            rows = dbcursor.fetchall()

            if dbcursor.rowcount > 0:
                error_msg = "error_username_taken"
                return render_template("joe/pages/login.html", msg = error_msg)
            
            # Check if email is already in use
            query = "SELECT * FROM carhireusers WHERE email = %s;"
            dbcursor.execute(query,[email])
            rows = dbcursor.fetchall()

            if dbcursor.rowcount > 0:
                error_msg = "error_email_taken"
                return render_template("joe/pages/login.html", msg = error_msg)

            # Otherwise, hash the password and create the account
            hashed_password = sha256_crypt.hash((str(password)))
            query = "INSERT INTO carhireusers (username, email, password_hash) VALUES (%s, %s, %s);"
            dbcursor.execute(query, [username, email, hashed_password])
            conn.commit()
            success_msg = "success_account_created"
            return render_template("joe/pages/login.html", msg = success_msg)

@app.route("/carhirelogin", methods=['POST', 'GET'])
def carhirelogin():
    if request.method == "POST":
        username = request.form["login-username"]
        password = request.form["login-password"]
        conn = get_connection()
        if conn != None:
            dbcursor = conn.cursor()
            # Check if username & password is in db
            query = "SELECT * FROM carhireusers WHERE username = %s AND password_hash = %s;"
            dbcursor.execute(query,[username, password])
            rows = dbcursor.fetchall()

            if dbcursor.rowcount > 0:
                success_msg = "success_logged_in"

                # Start session
                session['logged_in'] = True
                session['username'] = username

                # Get some extra details about the account
                dbcursor.execute("SELECT password_hash, usertype, userid FROM carhireusers WHERE username = %s;", [username])
                results = dbcursor.fetchone()

                # Set if user is admin or not and add details to session
                print(results[1])
                session['usertype'] = str(results[1])
                session['userid'] = str(results[2])

                return render_template("joe/pages/login.html", msg = success_msg)

            else:    
                error_msg = "error_invalid_login"
                return render_template("joe/pages/login.html", msg = error_msg)

@app.route("/logout")
def logout():
   session.clear()
   return render_template('joe/pages/login.html', msg = "logged_out")