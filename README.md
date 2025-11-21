About the Project
This is a terminal-based Student Management System written in Python.
It uses an SQLite database to store student information permanently.
Admin can perform all operations like:
Add a student
View all students
Update student details
Delete student
Search student by ID

The project also includes strong validation features such as phone number validation, email validation, grade validation, DOB validation, and password masking.


Validation System
Phone number must be exactly 10 digits
Email validation (format, TLD, @, domain checks)
DOB validation (DD-MM-YYYY format)
Grade validation (0–100 numeric only)
Gender validation (Male / Female only)
Unique Student ID

Database
SQLite database named students.db
Automatically created tables:
admin
students


Technologies Used
Technology	       Description
Python	         Core programming language
SQLite	        Lightweight database
msvcrt	        Windows-based password masking
os / sys	       System operations

