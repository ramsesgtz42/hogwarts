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
    
        
        
    
    
@app.route("/delete_class/<int:id>")
def delete_class(id):
    # query to delete student-class relationship
    query = "DELETE FROM Classes WHERE classID = '%s'"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/classes") 


@app.route("/edit_class/<int:id>", methods=["POST", "GET"])
def edit_class(id):
    if request.methon == "GET":
    # mySQL query to get info of class with passed ID
        query = "SELECT * from Classes WHERE classID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()    


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9115)) 
    app.run(port=port, debug=True) 