"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ?
        """
    db_cursor.execute(QUERY, (github,))
    row = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (
        row[0], row[1], row[2])


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.
    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    QUERY = """INSERT INTO Students VALUES (?, ?, ?)"""
    db_cursor.execute(QUERY, (first_name, last_name, github))
    db_connection.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    
    QUERY = """
        SELECT * 
        FROM Projects 
        WHERE title = ?
        """
    db_cursor.execute(QUERY, (title,))
    row = db_cursor.fetchone()
    print "Project id: %s Title: %s Description: %s Max Grade: %s" %(row[0], row[1], row[2], row[3])


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    QUERY = """
    SELECT grade
    FROM Grades
    WHERE project_title = ? AND student_github = ?
    """
    db_cursor.execute(QUERY, (title, github))
    row = db_cursor.fetchone()
    print type(row)
    print row
    print "Grade was %s" % row[0]


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    QUERY = """
        INSERT INTO Grades VALUES (?, ?, ?) 
        """
    db_cursor.execute(QUERY, (github, title, grade))
    db_connection.commit()
    print "Successfully assigned %s to %s" %(grade, github)

def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        # print command
        args = tokens[1:]
        # print args

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project_info":
            project = args[0]
            get_project_by_title(project)

        elif command == "get_grade":
            project, github_name = args
            get_grade_by_github_title(github_name, project)

        elif command == "add_grade":
            github, title, grade = args
            assign_grade(github, title, grade)



if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close()
