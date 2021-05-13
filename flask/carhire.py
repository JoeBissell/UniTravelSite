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

        print("Connected!")

        return render_template("joe/index.html", carDetails = results)

@app.route("/viewbookings")
def viewbookings():
    return render_template("joe/pages/viewbookings.html")

@app.route("/booktickets")
def booktickets():
    return render_template("joe/pages/makebookings.html")

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
                return render_template("joe/pages/login.html", msg = success_msg)

            else:    
                error_msg = "error_invalid_login"
                return render_template("joe/pages/login.html", msg = error_msg)
        

            


    return render_template("joe/pages/login.html")