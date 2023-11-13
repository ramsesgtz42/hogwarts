-- Data Definition Queries for Project Hogwarts
-- Group 108
-- Emily Reynolds
-- Alberto Ramses Gutierrez


SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;


-- Creates Houses Table
CREATE OR REPLACE TABLE Houses (
    houseID int UNIQUE NOT NULL,
    houseName varchar(15) UNIQUE NOT NULL,
    dormLocation varchar(30) UNIQUE NOT NULL,
    housePoints int NOT NULL DEFAULT 0,
    PRIMARY KEY (houseID)
);


-- Creates Professors Table
CREATE OR REPLACE TABLE Professors (
    professorID int AUTO_INCREMENT UNIQUE NOT NULL,
    profEmail varchar(50) UNIQUE NOT NULL,
    firstName varchar(25) NOT NULL,
    lastName varchar(25) NOT NULL,
    salary decimal(10,2) NOT NULL,
    startDate DATE NOT NULL,
    officeLocation varchar(50) UNIQUE NOT NULL,
    endDate DATE,
    isHeadOfHouse TINYINT(1) DEFAULT 0,
    houseID int,
    FOREIGN KEY (houseID) REFERENCES Houses(houseID),
    PRIMARY KEY (professorID)
);


-- Creates Classes Table
CREATE OR REPLACE TABLE Classes(
    classID int AUTO_INCREMENT UNIQUE NOT NULL,
    className varchar(25) NOT NULL,
    classLocation varchar(25) NOT NULL,
    classTime varchar(25) NOT NULL,
    professorID int,
    FOREIGN KEY(professorID) REFERENCES Professors(professorID),
    PRIMARY KEY(classID)
);


-- Creates Students Table
CREATE OR REPLACE TABLE Students (
    studentID int AUTO_INCREMENT UNIQUE NOT NULL,
    studEmail varchar(50) UNIQUE NOT NULL,
    firstName varchar(25) NOT NULL,
    lastName varchar(25) NOT NULL,
    classYear TINYINT(7) NOT NULL,
    isPrefect TINYINT(1) DEFAULT 0,
    houseID int NOT NULL,
    FOREIGN KEY (houseID) REFERENCES Houses(houseID),
    PRIMARY KEY (studentID)
);


-- Creates Point_assignments Table
CREATE OR REPLACE TABLE Point_Assignments(
    assignmentID int UNIQUE NOT NULL AUTO_INCREMENT,
    numOfPoints int NOT NULL,
    dateAssigned DATE NOT NULL,
    professorID int NOT NULL,
    studentID int NOT NULL,
    FOREIGN KEY (professorID) REFERENCES Professors(professorID),
    FOREIGN KEY (studentID) REFERENCES Students(studentID),
    PRIMARY KEY (assignmentID)
);


-- Creates Classes_to_Students Table
CREATE OR REPLACE TABLE Classes_To_Students(
    classID int,
    studentID int,
    FOREIGN KEY (classID) REFERENCES Classes(classID) ON DELETE CASCADE,
    FOREIGN KEY (studentID) REFERENCES Students(studentID) ON DELETE CASCADE,
    CONSTRAINT classesToStudentsID PRIMARY KEY (classID,studentID)
);


-- Inserting sample data into Houses table
INSERT INTO Houses (
    houseID,
    houseName,
    dormLocation
)
VALUES
(
    1,
    "Gryffindor",
    "Gryffindor Tower"
),
(
    2,
    "Hufflepuff",
    "Hufflepuff Basement"
),
(
    3,
    "Ravenclaw",
    "Ravenclaw Tower"
),
(
    4,
    "Slytherin",
    "Slytherin Dungeon"
);


-- Inserting sample data into Professors table
INSERT INTO Professors (
    profEmail,
    firstName,
    lastName,
    salary,
    startDate,
    officeLocation,
    isHeadofHouse,
    houseID
)
VALUES
(
    "ssnape@hogwarts.edu",
    "Severus",
    "Snape",
    100000,
    "1990-01-01",
    "Slytherin Tower Room 42",
    1,
    (SELECT houseID FROM Houses WHERE houseName = "Slytherin")
),
(
    "rhagrid@hogwarts.edu",
    "Rubeus",
    "Hagrid",
    60000,
    "1985-01-01",
    "Hagrid's Hut",
    0,
    (SELECT houseID FROM Houses WHERE houseName = "Gryffindor")
),
(
    "fflitwick@hogwarts.edu",
    "Filius",
    "Flitwick",
    100000,
    "1970-01-01",
    "Ravenclaw Tower Room 21",
    1,
    (SELECT houseID FROM Houses WHERE houseName = "Ravenclaw")
);


-- Inserting sample data into Classes table
INSERT INTO Classes (
    className,
    classLocation,
    classTime,
    professorID
)
VALUES 
(
    "Potions",
    "Dungeons Room 100",
    "Mon, Wed, Fri 8AM",
    (SELECT professorID from Professors WHERE firstName = "Severus" and lastName = "Snape")
),
(
    "Care of Magical Creatures",
    "Hagrid's Hut",
    "Tue, Thur 8AM",
    (SELECT professorID from Professors WHERE firstName = "Rubeus" and lastName = "Hagrid")
),
(
    "Charms",
    "Classroom 2E",
    "Mon, Wed, Fri 12PM",
    (SELECT professorID from Professors WHERE firstName = "Filius" and lastName = "Flitwick")
);


-- Inserting sample data into Students table
INSERT INTO Students (
    studEmail,
    firstName,
    lastName,
    classYear,
    isPrefect,
    houseID
)
VALUES 
(
    "hpotter@hogwarts.edu",
    "Harry",
    "Potter",
    3,
    0,
    (SELECT houseID FROM Houses WHERE houseName = "Gryffindor")
),
(
    "dmalfoy@hogwarts.edu",
    "Draco",
    "Malfoy",
    3,
    0,
    (SELECT houseID FROM Houses WHERE houseName = "Slytherin")
),
(
    "pweasley@hogwarts.edu",
    "Percy",
    "Weasley",
    7,
    1,
    (SELECT houseID FROM Houses WHERE houseName = "Gryffindor")
),
(
    "llovegood@hogwarts.edu",
    "Luna",
    "Lovegood",
    2,
    0,
    (SELECT houseID FROM Houses WHERE houseName = "Ravenclaw")
);


-- Inserting sample data into Point_assignments table
INSERT INTO Point_Assignments (
    numOfPoints,
    dateAssigned,
    professorID,
    studentID
)
VALUES
(
    15,
    "1993-05-05",
    (SELECT professorID FROM Professors WHERE firstName = "Severus" and lastName = "Snape"),
    (SELECT studentID FROM Students WHERE firstName = "Draco" and lastName = "Malfoy")
),
(
    15,
    "1993-05-06",
    (SELECT professorID FROM Professors WHERE firstName = "Rubeus" and lastName = "Hagrid"),
    (SELECT studentID FROM Students WHERE firstName = "Harry" and lastName = "Potter")
),
(
    15,
    "1993-05-07",
    (SELECT professorID FROM Professors WHERE firstName = "Filius" and lastName = "Flitwick"),
    (SELECT studentID FROM Students WHERE firstName = "Luna" and lastName = "Lovegood")
);


-- Inserting sample data into Classes_to_Students table
INSERT INTO Classes_To_Students(
    classID,
    studentID
)
VALUES
(
    (SELECT classID FROM Classes WHERE className = "Potions"),
    (SELECT studentID FROM Students WHERE firstName = "Harry" and lastName = "Potter")
),
(
    (SELECT classID FROM Classes WHERE className = "Potions"),
    (SELECT studentID FROM Students WHERE firstName = "Draco" and lastName = "Malfoy")
),
(
    (SELECT classID FROM Classes WHERE className = "Charms"),
    (SELECT studentID FROM Students WHERE firstName = "Harry" and lastName = "Potter")
),
(
    (SELECT classID FROM Classes WHERE className = "Charms"),
    (SELECT studentID FROM Students WHERE firstName = "Draco" and lastName = "Malfoy")
),
(
    (SELECT classID FROM Classes WHERE className = "Care of Magical Creatures"),
    (SELECT studentID FROM Students WHERE firstName = "Luna" and lastName = "Lovegood")
),
(
    (SELECT classID FROM Classes WHERE className = "Care of Magical Creatures"),
    (SELECT studentID FROM Students WHERE firstName = "Harry" and lastName = "Potter")
),
(
    (SELECT classID FROM Classes WHERE className = "Care of Magical Creatures"),
    (SELECT studentID FROM Students WHERE firstName = "Draco" and lastName = "Malfoy")
);


SET FOREIGN_KEY_CHECKS=1;
COMMIT;