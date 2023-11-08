from flask import Flask, render_template, json
import os
#import database.db_connector as db


# Configuration

app = Flask(__name__)
#db_connection = db.connect_to_database()

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/classes')
def classes():
    query = "SELECT classID, className, classLocation, classTime, CONCAT(Professors.firstName," ", Professors.lastName) as Professor FROM Classes"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = json.dumps(cursor.fetchall())
    return render_template("classes.j2", classes=results)

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 