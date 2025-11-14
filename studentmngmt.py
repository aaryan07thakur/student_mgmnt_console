import os
import sqlite3
import msvcrt
import sys


def initialize_database():
    #creating a database
    #admin table
    conn= sqlite3.connect("students.db")
    cursor=conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin(
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   username TEXT NOT NULL,
                   password TEXT NOT NULL
        )

    ''')

#student table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students(
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   student_id TEXT NOT NULL UNIQUE,
                   name TEXT NOT NULL,
                   grade TEXT NOT NULL,
                   gender TEXT NOT NULL,
                   dob TEXT NOT NULL,
                   degree TEXT NOT NULL,
                   stream TEXT NOT NULL,
                   phone INTEGER NOT NULL,
                   email TEXT NOT NULL,
                   address TEXT NOT NULL
        )

    ''')

#database ko data laie save garau n laie 
    conn.commit()
    conn.close()

initialize_database()

#validation of phone number======================================
def get_valid_phone(prompt="Enter Phone number: "):
    '''prompt repeatedly until user enter  exactly 10 digits .
    Return the phone as a string (keeps leading Zeros)
    '''
    while True:
        phone=input(prompt).strip()
        #check only digits
        if not phone.isdigit():
            print("Invalid phone number. please Enter a valid phone number (10 digits)")
            continue
        #check length exactly 10
        if len(phone)!=10:
            print("Invalid phone numbe.Please enter 10 digits phone number")
            continue
        #passed validation
        return phone
# =======================================================================

#Email validation function========================================
def get_valid_email(prompt="Enter Your Email: "):
    while True:
        email=input(prompt).strip()

        #Must contain exactly one "@"
        if email.count("@")!=1:
            print("Invalid email! Must contain '@'. ")
            continue

        username, domain= email.split("@")

        #Username must not be empty
        if len(username)==0:
            print("Invalid email! Username cannot be empty.")
            continue

        #Domain must not be empty
        if len(domain)==0:
            print("Invalid email! Domain cannot be empty.")
            continue

        #Domain must contain at least one dot
        if "." not in domain:
            print("invalid email! Domain must contain at least one '.' ")
            continue

        #Domain cannot start or end with dot
        if domain.startswith(".") or domain.endswith("."):
            print("Invalid email! Domain cannot start or end with '.' ")
            continue

        #check TLD(Top level Domain) length 
        tld=domain.split(".")[-1]
        if len(tld)<2 or len(tld)>4:
            print("Invalid email ! Domain extension(TLD) seems incorrect.")
            continue

        #passed all conditions
        return email


# ==================================================================================


#DoB validation==========================================================================
def get_valid_dob(prompt="Enter student Date of Birth (DD-MM-YYY): "):
    while True:
        dob=input(prompt).strip()
        parts=dob.split("-")
        if len(parts)!=3:
            print("Invalid format! use DD-MM-YYY.")
            continue
        day, month, year=parts
        if not (day.isdigit() and month.isdigit() and year.isdigit()):
            print("Invalid DOB! Day, Month, year must be numbers.")
            continue
        day,month,year=int(day),int(month),int(year)
        if not (1<=day <=31 and 1 <=month <=12 and year > 1900):
            print("Invalid DOB! Please enter realistic date. ")
            continue
        return dob

# ==========================================================================================

def input_password(prompt="Enter Password: "):
    """Custom password input with hidden characters."""
    print(prompt, end="", flush=True)
    password = ""

    while True:
        char = msvcrt.getwch()

        if char in ['\r', '\n']:  # Enter key pressed
            print()
            break
        elif char == '\b':  # Backspace
            if password:
                sys.stdout.write('\b \b')
                sys.stdout.flush()
                password = password[:-1]
        else:
            sys.stdout.write("*")
            sys.stdout.flush()
            password += char
    return password


#creating admin if admin is not exists
def create_admin_if_not_exists():
    conn=sqlite3.connect("students.db")

    cursor=conn.cursor()

    cursor.execute("select * from admin")

    existing_admin=cursor.fetchone()
    if not existing_admin:
        print("\n======= Admin Setup =====")
        username=input("Create Admin Username: ")
        password=input_password("Create Admin Password: ")

        cursor.execute("insert into admin(username,password)values(?,?)",(username,password))
        conn.commit() #to same data
        print("\n Admin created successfully! \n")
    conn.close()



def admin_login():
    conn=sqlite3.connect("students.db")
    cursor=conn.cursor()
    username=input("Enter UserName: ")
    password=input_password("Enter Password: ")
    cursor.execute("select * from admin where username=? and password=?",(username,password))

    admin=cursor.fetchone()

    conn.close()

    if admin:
        print("\n Login Successful! \n")
        return True
    else:
        print("\n Invalid Credentials! Try Again\n")
        return False

#adding students features
def add_student():
    conn=sqlite3.connect("students.db")
    cursor=conn.cursor()
    print("\n================ Add New Student===========================")
    student_id=input("Enter Student ID: ")

    #check student id already exists
    cursor.execute("SELECT * FROM students WHERE student_id=?",(student_id,))
    if cursor.fetchone():
        print("\nError:Student ID already exists!")
        conn.close()
        return
    
    name=input("Enter Student Name: ")
    grade=input("Enter Student Grade: ")
    gender=input("Enter Student Gender (Male/Female): ").strip().capitalize()
    while gender not in ["Male","Female"]:
        print("Invalid input! Please enter 'Male' or 'Female' ")
        gender=input("Enter Student Gender (Male/Female): ").strip().capitalize()

    dob=get_valid_dob("Enter Student Date of Birth (DD-MM-YYYY): ")
    degree=input("Enter the Student degree: ")
    stream=input("Enter Student Stream: ")
    phone=get_valid_phone("Enter Student phone Number: ")
    email=get_valid_email("Enter Your Email: ")
    address=input("Enter Student Address: ")

    try:
        cursor.execute('''
                       INSERT INTO students 
                       (student_id,name,grade,gender,dob,degree,stream,phone,email,address)
                       VALUES(?,?,?,?,?,?,?,?,?,?) ''',
                       (int(student_id),name,grade,gender,dob,degree,stream,int(phone),email,address))
        conn.commit()
        print("\n Student added successfully!")

    except sqlite3.IntegrityError:
        print("\nError: Student ID must be unique!")
    except Exception as e:
        print("\nSomething went wrong: ",e)
    conn.close()


#=============================================================================


def view_student():
    pass
def Update_student():
    pass
def Delete_student():
    pass


def show_menu():
    while True:
        print("\n" +"="*100)
        print("                 MAIN MENU                   ")
        print("="*100)
        print("1. Add Student")
        print("2. View Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Logout Student")
        print("="*100)

        choice=input("Enter your choise (1-5): ")
        if choice == "1":
            add_student()
        elif choice=="2":
            view_student()
        elif choice=="3":
            Update_student()
        elif choice=="4":
            Delete_student()
        elif choice=="5":
            print("\n Logging out....\n")
            break
        else:
            print("\n Invalid Choice! Please enter a valid option.\n")
        


def clear_screen():
    os.system("cls" if os.name== 'nt' else 'clear')

#cleating heading wiht 100 == and in middle project name
def show_heading():
    print("="*100)
    print("                             STUDENT MANAGEMENT SYSTEM           ")
    print("="*100)
    print("\n")



def main():
    clear_screen()
    show_heading()
    create_admin_if_not_exists()

    while True:
        if admin_login():
            show_menu()
            break



#calling main function 
#first ma main function run garna ko lagie hami le main hamro first function ho vane r vannu par x 
if __name__=="__main__":
    main()






