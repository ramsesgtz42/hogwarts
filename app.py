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
db_connection = db.connect_to_database()
db_connection.ping(True)
mysql = MySQL(app)

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/houses', methods=["POST", "GET"])
def houses():
    if request.method == "POST":
        if request.form.get("addHouse"):
            houseName = request.form["houseName"]
            dormLocation = request.form["dormLocation"]

            query = "INSERT INTO Houses (houseName, dormLocation) VALUES ('%s', '%s')" % (houseName, dormLocation)
            db.execute_query(db_connection, query)
        
        return redirect("/houses")
        
    if request.method == "GET":
        #query to fill houses table data
        query = "SELECT houseID, houseName, dormLocation FROM Houses"
        cursor = db.execute_query(db_connection, query)
        results = cursor.fetchall()

    return render_template("houses.html", houses=results)

@app.route('/delete_houses/<int:id>')
def delete_house(id):
    #query to delete house
    query = "DELETE FROM Houses WHERE houseID = '%s'" % (id)
    db.execute_query(db_connection, query)
    return redirect("/houses")

@app.route('/edit_houses/<int:id>', methods=["POST", "GET"])
def edit_house(id):
    if request.method == "POST":
        if request.form.get("Edit_House"):
            houseID = request.form["houseID"]
            houseName = request.form["houseName"]
            dormLocation = request.form["dormLocation"]

            #query to update House information
            query = "UPDATE Houses SET houseName = '%s', dormLocation = '%s' WHERE houseID = '%s'" % (houseName, dormLocation, houseID)
            db.execute_query(db_connection, query)
            return redirect("/houses")
        
    if request.method == "GET":
        query = "SELECT * from Houses WHERE houseID = '%s'" % (id)
        cursor = db.execute_query(db_connection, query)
        data = cursor.fetchall()

    return render_template("edit_houses.j2", data=data)

@app.route('/points', methods=["POST", "GET"])
def points():
    return render_template("points.html")

@app.route('/professors', methods=["POST", "GET"])
def professors():
    if request.method == "POST":
        if request.form.get("addProfessor"):
            profEmail = request.form["email"]
            firstName = request.form["fname"]
            lastName = request.form["lname"]
            salary = request.form["salary"]
            startDate = request.form["startdate"]
            officeLocation = request.form["officelocation"]
            isHeadOfHouse = request.form["isheadofhouse"]
            houseID = request.form["house"]

        if houseID == "":
            #query if professor is Houseless
            query = "INSERT INTO Professors (profEmail, firstName, lastName, salary, startDate, officeLocation, isHeadOfHouse) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (profEmail, firstName, lastName, salary, startDate, officeLocation, isHeadOfHouse)
            db.execute_query(db_connection, query)
        else:
            #query if all fields are filled
            query = "INSERT INTO Professors (profEmail, firstName, lastName, salary, startDate, officeLocation, isHeadOfHouse, houseID) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (profEmail, firstName, lastName, salary, startDate, officeLocation, isHeadOfHouse, houseID)
            db.execute_query(db_connection, query)
        
        return redirect("/professors")

    if request.method == "GET":
        #query to get all professor data
        query = 'SELECT professorID as ID, CONCAT(firstName," ", lastName) as Name, profEmail as Email, officeLocation as Office, startDate, endDate, salary, IFNULL(Houses.houseName, "Houseless") as house, isHeadofHouse as "Head of House" FROM Professors INNER JOIN Houses ON Professors.houseID = Houses.houseID'
        cursor = db.execute_query(db_connection, query)
        results = cursor.fetchall()

        #query to fill house dropdown menu data when adding professor
        query2 = 'SELECT houseID, houseName FROM Houses'
        cursor = db.execute_query(db_connection, query2)
        houses = cursor.fetchall()

        return render_template("professors.html", Professors=results, Houses=houses)

@app.route("/edit_professors/<int:id>", methods=["POST", "GET"])
def edit_professor(id):
    
    if request.method == "POST":
        if request.form.get("Edit_Professor"):
            professorID = request.form["professorID"]
            profEmail = request.form["profEmail"]
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            salary = request.form["salary"]
            startDate = request.form["startDate"]
            officeLocation = request.form["officeLocation"]
            endDate = request.form["endDate"]
            isHeadOfHouse = request.form["isHeadOfHouse"]
            houseID = request.form["houseID"]

            if houseID == "":
                #query if professor is Houseless
                query = "UPDATE Professors SET profEmail = '%s', firstName = '%s', lastName = '%s', salary = '%s', startDate = '%s', officeLocation = '%s', endDate = '%s', isHeadOfHouse = '%s', houseID = NULL WHERE professorID = '%s'" % (profEmail, firstName, lastName, salary, startDate, officeLocation, endDate, isHeadOfHouse, professorID)
                db.execute_query(db_connection, query)
            elif endDate == "":
                #query if enddate is left Null
                query = "UPDATE Professors SET profEmail = '%s', firstName = '%s', lastName = '%s', salary = '%s', startDate = '%s', officeLocation = '%s', endDate = NULL, isHeadOfHouse = '%s', houseID = '%s' WHERE professorID = '%s'" % (profEmail, firstName, lastName, salary, startDate, officeLocation, isHeadOfHouse, houseID, professorID)
                db.execute_query(db_connection, query)
            elif houseID and endDate == "":
                #query if houseless and enddate left Null:
                query = "UPDATE Professors SET profEmail = '%s', firstName = '%s', lastName = '%s', salary = '%s', startDate = '%s', officeLocation = '%s', endDate = NULL, isHeadOfHouse = '%s', houseID = NULL WHERE professorID = '%s'" % (profEmail, firstName, lastName, salary, startDate, officeLocation, isHeadOfHouse, professorID)
                db.execute_query(db_connection, query)
            else:
                query = "UPDATE Professors SET profEmail = '%s', firstName = '%s', lastName = '%s', salary = '%s', startDate = '%s', officeLocation = '%s', endDate = '%s', isHeadOfHouse = '%s', houseID = '%s' WHERE professorID = '%s'" % (profEmail, firstName, lastName, salary, startDate, officeLocation, endDate, isHeadOfHouse, houseID, professorID)
                db.execute_query(db_connection, query)
            
            return redirect("/professors")
        
    if request.method == "GET":
        #query to get professor's info
        query = "SELECT * from Professors WHERE professorID = '%s'" % (id)
        cursor = db.execute_query(db_connection, query)
        data = cursor.fetchall()

        #query to populate house dropdown menu
        query = "SELECT houseID, houseName from Houses"
        cursor = db.execute_query(db_connection, query)
        houses = cursor.fetchall()

    return render_template("edit_professors.j2", data=data, Houses=houses)

@app.route("/delete_professors/<int:id>")
def delete_professor(id):
    #query to  delete professor
    query = "DELETE FROM Professors WHERE professorID = '%s'" % (id)
    db.execute_query(db_connection, query)
    return redirect("/professors")

@app.route('/students', methods=["POST", "GET"])
def students():
    if request.method == "POST":
        if request.form.get("addStudent"):
            studEmail = request.form["studEmail"]
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            classYear = request.form["classYear"]
            houseID = request.form["houseID"]
            isPrefect = request.form["isPrefect"]

            query = "INSERT INTO Students (studEmail, firstName, lastName, classYear, houseID, isPrefect) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (studEmail, firstName, lastName, classYear, houseID, isPrefect)
            db.execute_query(db_connection, query)

        return redirect("/students")

    if request.method == "GET":
        #query to fill student table
        query = 'SELECT studentID, firstName, lastName, studEmail as Email, classYear, Houses.houseName as House FROM Students INNER JOIN Houses ON Students.houseID = Houses.houseID'
        cursor = db.execute_query(db_connection, query)
        results = cursor.fetchall()

        #query to fill house dropdown menu for adding new student:
        query = 'SELECT houseID, houseName FROM Houses'
        cursor = db.execute_query(db_connection, query)
        houses = cursor.fetchall()

    return render_template("students.html", students=results, houses=houses)

@app.route("/edit_students/<int:id>", methods=["POST", "GET"])
def edit_student(id):
    if request.method == "GET":
        #query to get students information
        query = "SELECT * from Students WHERE studentID = '%s'" % (id)
        cursor = db.execute_query(db_connection, query)
        data = cursor.fetchall()

        #query to get house information for dropdown menu
        query = "SELECT houseID, houseName from Houses"
        cursor = db.execute_query(db_connection, query)
        houses = cursor.fetchall()

        return render_template("edit_students.j2", data=data, houses=houses)
    
    if request.method == "POST":
        if request.form.get("Edit_Student"):
            studentID = request.form["studentID"]
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            studEmail = request.form["studEmail"]
            classYear = request.form["classYear"]
            isPrefect = request.form["isPrefect"]
            houseID = request.form["houseID"]

            query = "UPDATE Students SET firstName = '%s', lastName = '%s', studEmail = '%s', classYear = '%s', isPrefect = '%s', houseID = '%s' WHERE studentID = '%s'" % (firstName, lastName, studEmail, classYear, isPrefect, houseID, studentID)
            db.execute_query(db_connection, query)

            return redirect("/students")

@app.route('/delete_students/<int:id>')
def delete_student(id):
    #query to delete student
    query = "DELETE FROM Students WHERE studentID = '%s'" % (id)
    db.execute_query(db_connection, query)
    return redirect("/students")


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
                query = "INSERT INTO Classes (className, classLocation, classTime) VALUES ('%s', '%s', '%s')" % (className, classLocation, classTime)
                cursor = db.execute_query(db_connection, query)
            
            else:
                # query for all fields filled
                query = "INSERT INTO Classes (className, classLocation, classTime, professorID) VALUES ('%s', '%s', '%s', '%s')" % (className, classLocation, classTime, professorID)
                cursor = db.execute_query(db_connection, query)

            return redirect("/classes")
        

    if request.method == "GET":
        #query to fill first table for class info
        query = 'SELECT classID, className as Class, classLocation as Location, classTime as Time, CONCAT(Professors.firstName," ", Professors.lastName) as Professor FROM Classes INNER JOIN Professors ON Classes.professorID = Professors.professorID'
        cursor = db.execute_query(db_connection, query)
        results = cursor.fetchall()

        #query to fill dropdown menu for adding new class
        query3 = 'SELECT Professors.professorID as ID, CONCAT(Professors.firstName," ", Professors.lastName) as Professor FROM Professors'
        cursor3 = db.execute_query(db_connection, query3)
        results3 = cursor3.fetchall()

        #query to show students enrolled in classes
        query2 = 'SELECT Classes.className as Class, CONCAT(Students.firstName," ", Students.lastName) as Student FROM Classes_To_Students JOIN Classes ON Classes_To_Students.classID = Classes.classID JOIN Students ON Classes_To_Students.studentID = Students.studentID'
        cursor2 = db.execute_query(db_connection, query2)
        results2 = cursor2.fetchall()
        return render_template("classes.j2", Classes=results, student_class=results2, professors = results3)
            
            
    
@app.route("/delete_classes/<int:id>")
def delete_class(id):
    # query to delete class
    query = "DELETE FROM Classes WHERE classID = '%s'" % (id)
    db.execute_query(db_connection, query)
    return redirect("/classes") 


@app.route("/edit_classes/<int:id>", methods=["POST", "GET"])
def edit_class(id):
    if request.method == "POST":
        if request.form.get("Edit_Class"):
            classID = request.form["classID"]
            className = request.form["className"]
            classLocation = request.form["classLocation"]
            classTime = request.form["classTime"]
            professorID = request.form["professor"]

            if professorID == "":
                #query if professor field is empty
                query = "UPDATE Classes SET className = '%s', classLocation = '%s', classTime = '%s', professorID = NULL WHERE classID = '%s'" % (className, classLocation, classTime, classID)
                db.execute_query(db_connection, query)
            else:
                query = "UPDATE Classes SET className = '%s', classLocation = '%s', classTime = '%s', professorID = '%s' WHERE classID = '%s'" % (className, classLocation, classTime, professorID, classID)
                db.execute_query(db_connection, query)
            
            return redirect("/classes")
        
    if request.method == "GET":
        # mySQL query to get info of class with passed ID
        query = "SELECT * from Classes WHERE classID = '%s'" % (id)
        cur = db.execute_query(db_connection, query)
        data = cur.fetchall()

        #mySQL query to populate Professor dropdown menu
        query2 = "SELECT professorID as ID, CONCAT(Professors.firstName,' ', Professors.lastName) as Professor FROM Professors"
        cur2 = db.execute_query(db_connection, query2)
        professorData = cur2.fetchall()

    return render_template("edit_classes.j2", data=data, professors=professorData)



# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9115)) 
    app.run(port=port, debug=True) 