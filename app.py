from flask import Flask, render_template, json, redirect, request
from flask_mysqldb import MySQL
import os
import database.db_connector as db


      # Citation for app.py, classes.j2, main.j2, edit_classes.j2
      # Date: 11/16/23
      # Based on: OSU CS340 Flask Starter App 
      # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app


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

@app.route('/houses')
def houses():
    return render_template("houses.html")

@app.route('/points')
def points():
    return render_template("points.html")

@app.route('/professors')
def professors():
    return render_template("professors.html")

@app.route('/students')
def students():
    return render_template("students.html")

@app.route('/classes', methods=["POST", "GET"])
def classes():
    if request.method == "POST":
        #if add class button is clicked
        if request.form.get("addClass"):
            className = request.form["name"]
            classLocation = request.form["location"]
            classTime = request.form["time"]
            professorID = request.form["professor"]

            if professorID == "":
                # query if professor field left empty
                query = "INSERT INTO Classes (className, classLocation, classTime) VALUES (%s, %s, %s)" 
                cursor = mysql.connection.cursor()
                cursor.execute(query, (className, classLocation, classTime))
                mysql.connection.commit()
            
            else:
                # query for all fields filled
                query = "INSERT INTO Classes (className, classLocation, classTime, professorID) VALUES (%s, %s, %s, %s)"
                cursor = mysql.connection.cursor()
                cursor.execute(query, (className, classLocation, classTime, professorID))
                mysql.connection.commit()

            return redirect("/classes")
        

    if request.method == "GET":
        #query to fill first table for class info
        query = 'SELECT classID, className as Class, classLocation as Location, classTime as Time, CONCAT(Professors.firstName," ", Professors.lastName) as Professor FROM Classes INNER JOIN Professors ON Classes.professorID = Professors.professorID'
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        #query to fill dropdown menu for adding new class
        query3 = 'SELECT Professors.professorID as ID, CONCAT(Professors.firstName," ", Professors.lastName) as Professor FROM Professors'
        cursor3 = db.execute_query(db_connection=db_connection, query=query3)
        results3 = cursor3.fetchall()

        #query to show students enrolled in classes
        query2 = 'SELECT Classes.className as Class, CONCAT(Students.firstName," ", Students.lastName) as Student FROM Classes_To_Students JOIN Classes ON Classes_To_Students.classID = Classes.classID JOIN Students ON Classes_To_Students.studentID = Students.studentID'
        cursor2 = db.execute_query(db_connection=db_connection, query=query2)
        results2 = cursor2.fetchall()
        return render_template("classes.j2", Classes=results, student_class = results2, professors = results3)
    
        
        
    
    
@app.route("/delete_classes/<int:id>")
def delete_class(id):
    # query to delete class
    query = "DELETE FROM Classes WHERE classID = '%s'"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/classes") 


@app.route("/edit_classes/<int:id>", methods=["POST", "GET"])
def edit_class(id):
    if request.method == "GET":
        # mySQL query to get info of class with passed ID
        query = "SELECT * from Classes WHERE classID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        #mySQL query to populate Professor dropdown menu
        query2 = "SELECT professorID as ID, CONCAT(Professors.firstName,' ', Professors.lastName) as Professor FROM Professors"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        professorData = cur.fetchall()

        return render_template("edit_classes.j2", data=data, professors=professorData)

    if request.method == "POST":
        if request.form.get("Edit_Class"):
            classID = request.form["classID"]
            className = request.form["className"]
            classLocation = request.form["classLocation"]
            classTime = request.form["classTime"]
            professorID = request.form["professor"]

            if professorID == "":
                #query if professor field is empty
                query = "UPDATE Classes SET className = %s, classLocation = %s, classTime = %s, professorID = NULL WHERE classID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (className, classLocation, classTime, classID))
                mysql.connection.commit()

            else:
                query = "UPDATE Classes SET className = %s, classLocation = %s, classTime = %s, professorID = %s WHERE classID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (className, classLocation, classTime, professorID, classID))
                mysql.connection.commit()
            
            return redirect("/classes")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9115)) 
    app.run(port=port, debug=True) 