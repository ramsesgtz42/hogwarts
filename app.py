from flask import Flask, render_template, json, redirect, request
from flask_mysqldb import MySQL
import os
import database.db_connector as db


# Configuration

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_gutiealb'
app.config['MYSQL_PASSWORD'] = '4429' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_gutiealb'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
db_connection = db.connect_to_database()

mysql = MySQL(app)

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/classes')
def classes():
    query = "SELECT * FROM Classes"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("classes.j2", Classes=results)

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112)) 
    app.run(port=port, debug=True) 