from __main__ import app, get_connection
from flask import Flask, render_template, request, session, redirect, url_for, escape, abort, jsonify, redirect
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

@app.route("/carhirelogin")
def carhirelogin():
    return render_template("joe/pages/login.html")