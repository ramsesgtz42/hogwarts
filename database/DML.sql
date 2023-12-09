-- Database Manipulation Queries for Project Hogwarts

-- get Student information to populate Student page
SELECT studentID, firstName, lastName, studEmail as Email, classYear, Houses.houseName as House FROM Students
INNER JOIN Houses ON Students.houseID = Houses.houseID;

--get Student information to populate dropdown menu on Class page
SELECT studentID, CONCAT(firstName," ",lastName) as Name, studEmail as Email, classYear, Houses.houseName as House FROM Students 
INNER JOIN Houses ON Students.houseID = Houses.houseID;

-- get Professor information to populate Professors page
SELECT professorID as ID, CONCAT(firstName," ", lastName) as Name, profEmail as Email, officeLocation as Office, startDate, endDate, salary, IFNULL(Houses.houseName, "Houseless") as house, isHeadofHouse as House Head FROM Professors 
INNER JOIN Houses ON Professors.houseID = Houses.houseID;

-- get Classes information to populate Classes page
SELECT classID, className as Class, classLocation as Location, classTime as Time, CONCAT(Professors.firstName," ", Professors.lastName) as Professor FROM Classes
INNER JOIN Professors ON Classes.professorID = Professors.professorID;

-- get Professor information to populate dropdown menu on Classes page
SELECT Professors.professorID as ID, CONCAT(Professors.firstName," ", Professors.lastName) as Professor FROM Professors;

-- get Point Assignment information to populate Points page
SELECT assignmentID, numOfPoints, dateAssigned, CONCAT(Professors.firstName," ", Professors.lastName) as Professor, CONCAT(Students.firstName," ", Students.lastName) as Student FROM Point_Assignments
JOIN Professors ON Point_Assignments.professorID = Professors.professorID
JOIN Students ON Point_Assignments.studentID = Students.studentID;

--get House information to populate Houses page
SELECT houseID, houseName, dormLocation as Dorm FROM Houses;

--get Classes_To_Students information to view Enrolled Students in Student page
SELECT Classes.className as Class, CONCAT(Students.firstName," ", Students.lastName) as Student FROM Classes_To_Students 
JOIN Classes ON Classes_To_Students.classID = Classes.classID 
JOIN Students ON Classes_To_Students.studentID = Students.studentID;


--Enroll a new Student
INSERT INTO Students (studEmail, firstName, lastName, classYear, houseID)
VALUES (:emailInput, :fnameInput, :lnameInput, :yearInput, :houseInput);

--Hire a new Professor
INSERT INTO Professors (profEmail, firstName, lastName, salary, startDate, officeLocation, houseID)
VALUES (:emailInput, :fnameInput, :lnameInput, :salaryInput, :startInput, :officeInput, :houseInput);

--Add a new Class
INSERT INTO Classes (className, classLocation, classTime, professorID)
VALUES (:nameInput, :locationInput, :timeInput, :professorInput);

--Add a new Class without Professor
INSERT INTO Classes (className, classLocation, classTime) 
VALUES (%s, %s, %s);

--Add a new House (dont do this!)
INSERT INTO Houses (houseName, dormLocation)
VALUES (:nameInput, :locationInput);

--Create a new Point Assignment record
INSERT INTO Point_Assignments (numOfPoints, dateAssigned, professorID, studentID)
VALUES (:pointInput, :dateInput, :professorInput, :studentInput);

--Enroll a Student into a Class
INSERT INTO Classes_To_Students(classID, studentID)
VALUES (:classInput, :studentInput);


--Update Student data based on submission page
UPDATE Students SET firstName = :fname, lastName = :lname, 
                    studEmail = :emailInput, classYear = :yearInput, 
                    isPrefect = :prefectInput, houseID = :houseInput 
                    WHERE studentID = :studentID_form;

--Update Professors data based on submission page
UPDATE Professors SET firstName = :fnameInput, lastName = :lnameInput, 
                    profEmail = :emailInput, houseID = :houseInput
                    salary = :salaryInput, officeLocation = :officeInput
                    endDate = :endInput, isHeadOfHouse = :headInput
                    WHERE professorID = :professorID_form;

--Update Classes Data based on submission page
UPDATE Classes SET className = :nameInput, classLocation = :locationInput,
                    classTime = :timeInput, professorID = :professorInput
                    WHERE classID = :classID_form;

--Update House Data
UPDATE Houses SET houseName = '%s', dormLocation = '%s' WHERE houseID = '%s';

--Update Point Assignment Data
UPDATE Point_Assignments SET numOfPoints = '%s', dateAssigned = '%s', professorID = '%s', studentID = '%s' WHERE assignmentID = '%s';

--Update Classes_To_Students Data
UPDATE Classes_To_Students SET classID = '%s', studentID = '%s' WHERE classID = '%s';

--Withdraw a Student
DELETE FROM Students WHERE studentID = :idInput;

--Remove a Professor
DELETE FROM Professors WHERE professorID = '%s';

--Delete a House
DELETE FROM Houses WHERE houseID = '%s';

--Drop a Student's Class
DELETE FROM Classes_To_Students WHERE Classes.classId = '%s'  AND Students.studentId = '%s'; 

--Delete a Class
DELETE FROM Classes WHERE classId = :classInput;

--Delete a Point Assignment
DELETE FROM Point_Assignments WHERE assignmentID = '%s';