import hashlib
import sqlite3
from sqlite3 import Error

# Function to create a connection with SQLite
def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('hospital.db') # create a database in disk
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

# Function to close the connection with SQLite
def close_connection(conn):
    conn.close()
    
# Function to create a table
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        
# Function to create a user
def create_user(conn, username, password):
    hash_password = hashlib.sha256(password.encode()).hexdigest()
    sql = ''' INSERT INTO users(username,password)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (username, hash_password))
    return cur.lastrowid

# Function to authenticate a user
def authenticate_user(conn, username, password):
    hash_password = hashlib.sha256(password.encode()).hexdigest()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password))

    rows = cur.fetchall()

    if rows:
        return "User authenticated successfully"
    else:
        return "Invalid username or password"

# Function to update a user's password
def update_user(conn, username, new_password):
    hash_password = hashlib.sha256(new_password.encode()).hexdigest()
    sql = ''' UPDATE users
              SET password = ?
              WHERE username = ?'''
    cur = conn.cursor()
    cur.execute(sql, (hash_password, username))
    conn.commit()
    return "User updated successfully"

# Function to delete a user
def delete_user(conn, username):
    sql = ''' DELETE FROM users WHERE username = ?'''
    cur = conn.cursor()
    cur.execute(sql, (username,))
    conn.commit()
    return "User deleted successfully"

# Function to retrieve a user's information
def get_user(conn, username):
    sql = ''' SELECT * FROM users WHERE username = ?'''
    cur = conn.cursor()
    cur.execute(sql, (username,))
    user = cur.fetchone()
    if user is None:
        return "User not found"
    else:
        return user
    
# Function to retrieve all users' information
def get_all_users(conn):
    sql = ''' SELECT * FROM users'''
    cur = conn.cursor()
    cur.execute(sql)
    users = cur.fetchall()
    return users

class Admin:
    def __init__(self, name, admin_id):
        self.name = name
        self.admin_id = admin_id
        self.doctors = []
        self.nurses = []
        self.support_staffs = []

    def add_doctor(self, name, doctor_id, specialty):
        new_doctor = Doctor(name, doctor_id, specialty)
        self.doctors.append(new_doctor)
        return f"Doctor {name} added successfully"

    def add_nurse(self, name, nurse_id, specialty):
        new_nurse = Nurse(name, nurse_id, specialty)
        self.nurses.append(new_nurse)
        return f"Nurse {name} added successfully"

    def add_support_staff(self, name, support_staff_id, department):
        new_support_staff = SupportStaff(name, support_staff_id, department)
        self.support_staffs.append(new_support_staff)
        return f"Support staff {name} added successfully"

    def remove_doctor(self, doctor_id):
        for doctor in self.doctors:
            if doctor.doctor_id == doctor_id:
                self.doctors.remove(doctor)
                return f"Doctor {doctor.name} removed successfully"
        return "Doctor not found"

    def remove_nurse(self, nurse_id):
        for nurse in self.nurses:
            if nurse.nurse_id == nurse_id:
                self.nurses.remove(nurse)
                return f"Nurse {nurse.name} removed successfully"
        return "Nurse not found"

    def remove_support_staff(self, support_staff_id):
        for support_staff in self.support_staffs:
            if support_staff.support_staff_id == support_staff_id:
                self.support_staffs.remove(support_staff)
                return f"Support staff {support_staff.name} removed successfully"
        return "Support staff not found"

    def get_all_staff(self):
        return {
            'doctors': [(doctor.name, doctor.doctor_id) for doctor in self.doctors],
            'nurses': [(nurse.name, nurse.nurse_id) for nurse in self.nurses],
            'support_staffs': [(support_staff.name, support_staff.support_staff_id) for support_staff in self.support_staffs]
        }
        
    def update_doctor_schedule(self, doctor_id, day, start_time, end_time):
        for doctor in self.doctors:
            if doctor.doctor_id == doctor_id:
                doctor.assign_schedule(day, start_time, end_time)
                return f"Schedule for Doctor {doctor.name} updated successfully"
        return "Doctor not found"

    def update_nurse_schedule(self, nurse_id, day, start_time, end_time):
        for nurse in self.nurses:
            if nurse.nurse_id == nurse_id:
                nurse.assign_schedule(day, start_time, end_time)
                return f"Schedule for Nurse {nurse.name} updated successfully"
        return "Nurse not found"

# Patient class
class Patient:
    def __init__(self, name, age, gender, address, phone, medical_history=None):
        self.name = name
        self.age = age
        self.gender = gender
        self.address = address
        self.phone = phone
        self.medical_history = medical_history if medical_history else []

    def request_appointment(self, doctor, date):
        return f"Patient {self.name} is requesting an appointment with Doctor {doctor.name} on {date}"

# For managing attendance and leave, we'll add a simple dictionary to track this.
class MedicalStaff:
    def __init__(self, name, staff_id):
        self.name = name
        self.staff_id = staff_id
        self.attendance = {}

    def manage_attendance(self, date):
        self.attendance[date] = "Present"

    def manage_leave(self, start_date, end_date):
        for date in range(start_date, end_date):
            self.attendance[date] = "Absent"

# Doctor class
class Doctor(MedicalStaff):
    def __init__(self, name, doctor_id, specialty):
        super().__init__(name, doctor_id)
        self.specialty = specialty
        self.doctor_id = doctor_id
        self.schedule = {}

    def assign_schedule(self, day, start_time, end_time):
        self.schedule[day] = (start_time, end_time)

    def consult_patient(self, patient):
        return f"Doctor {self.name} is consulting patient {patient.name}"

# Nurse class
class Nurse(MedicalStaff):
    def __init__(self, name, nurse_id, specialty):
        super().__init__(name, nurse_id)
        self.specialty = specialty
        self.schedule = {}
        self.nurse_id = nurse_id

    def assign_schedule(self, day, start_time, end_time):
        self.schedule[day] = (start_time, end_time)

    def administer_medication(self, patient, medication):
        return f"Nurse {self.name} is administering {medication} to patient {patient.name}"

# SupportStaff class
class SupportStaff(MedicalStaff):
    def __init__(self, name, support_staff_id, department):
        super().__init__(name, support_staff_id)
        self.department = department

    def manage_resources(self, resource):
        return f"Support staff {self.name} is managing resource {resource}"

# Appointment class
class Appointment:
    def __init__(self, patient, doctor, date, time):
        self.patient = patient
        self.doctor = doctor
        self.date = date
        self.time = time

# MedicalHistory class
class MedicalHistory:
    def __init__(self, patient, primary_doctor, records=None):
        self.patient = patient
        self.primary_doctor = primary_doctor
        self.records = records if records else []

    def add_record(self, date, description, doctor):
        new_record = {
            'date': date,
            'description': description,
            'doctor': doctor
        }
        self.records.append(new_record)

    def get_records(self):
        return self.records

# Invoice class
class Invoice:
    def __init__(self, patient, services, total):
        self.patient = patient
        self.services = services
        self.total = total
        self.paid = False

    def mark_paid(self):
        self.paid = True

# Function to generate an invoice
def generate_invoice(patient, services, total):
    invoice = Invoice(patient, services, total)
    return invoice

# Function to manage payment
def manage_payment(invoice, amount):
    if amount >= invoice.total:
        invoice.mark_paid()

# Function to create a user
def create_user(conn, username, password):
    hash_password = hashlib.sha256(password.encode()).hexdigest()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))

    if cur.fetchone() is not None:
        return "Username already exists"
    else:
        sql = ''' INSERT INTO users(username,password)
                  VALUES(?,?) '''
        cur.execute(sql, (username, hash_password))
        return "User created successfully"

# Function to authenticate a user
def authenticate_user(conn, username, password):
    hash_password = hashlib.sha256(password.encode()).hexdigest()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password))

    if cur.fetchone() is not None:
        return "User authenticated successfully"
    else:
        return "Invalid username or password"
    
# Function to insert multiple users for testing
def insert_test_users(conn):
    users = [
        ('testuser1', 'password1'),
        ('testuser2', 'password2'),
        ('testuser3', 'password3'),
        # Add more users as needed
    ]

    for user in users:
        create_user(conn, user[0], user[1])

def main():
    conn = create_connection()

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY,
                                    username text NOT NULL,
                                    password text NOT NULL
                                ); """

    if conn is not None:
        create_table(conn, sql_create_users_table)
    else:
        print("Error! cannot create the database connection.")
        
    admin = Admin("Admin", 1)

    # User management
    while True:
        print("1. Create user")
        print("2. Authenticate user")
        print("3. Update user password")
        print("4. Delete user")
        print("5. Get user")
        print("6. Get all users")
        print("7. Assign a role to a user")
        print("8. Make an admin")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(create_user(conn, username, password))
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(authenticate_user(conn, username, password))
        elif choice == '3':
            username = input("Enter username: ")
            new_password = input("Enter new password: ")
            print(update_user(conn, username, new_password))
        elif choice == '4':
            username = input("Enter username: ")
            print(delete_user(conn, username))
        elif choice == '5':
            username = input("Enter username: ")
            print(get_user(conn, username))
        elif choice == '6':
            users = get_all_users(conn)
            for user in users:
                print(user)
        elif choice == '7':
            while True:
                username = input("Enter username: ")
                print("1. Convert to Doctor")
                print("2. Convert to Nurse")
                print("3. Convert to Patient")
                print("4. Back to main menu")
                role_choice = input("Enter your choice: ")
                if role_choice == '1':
                    staff_id = int(input("Enter the doctor's staff ID: "))
                    specialty = input("Enter the doctor's specialty: ")

                    doctor = Doctor(username, staff_id, specialty)
                elif role_choice == '2':
                    staff_id = int(input("Enter the nurse's staff ID: "))
                    specialty = input("Enter the nurse's specialty: ")
                    
                    nurse = Nurse(username, staff_id, specialty)
                elif role_choice == '3':
                    age = int(input("Enter the patient's age: "))
                    gender = input("Enter the patient's gender: ")
                    address = input("Enter the patient's address: ")
                    phone = input("Enter the patient's phone number: ")

                    patient = Patient(username, age, gender, address, phone)
                elif role_choice == '4':
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 3.")
        elif choice == '8':
            while True:
                print("\n1. Add Doctor")
                print("2. Add Nurse")
                print("3. Add Support Staff")
                print("4. Remove Doctor")
                print("5. Remove Nurse")
                print("6. Remove Support Staff")
                print("7. Get All Staff")
                print("8. Update Doctor Schedule")
                print("9. Update Nurse Schedule")
                print("0. Exit")
                
                choice = input("\nEnter your choice: ")

                if choice == '1':
                    name = input("Enter Doctor's Name: ")
                    doctor_id = int(input("Enter Doctor's ID: "))
                    specialty = input("Enter Doctor's Specialty: ")
                    print(admin.add_doctor(name, doctor_id, specialty))

                elif choice == '2':
                    name = input("Enter Nurse's Name: ")
                    nurse_id = int(input("Enter Nurse's ID: "))
                    specialty = input("Enter Nurse's Specialty: ")
                    print(admin.add_nurse(name, nurse_id, specialty))

                elif choice == '3':
                    name = input("Enter Support Staff's Name: ")
                    support_staff_id = int(input("Enter Support Staff's ID: "))
                    department = input("Enter Support Staff's Department: ")
                    print(admin.add_support_staff(name, support_staff_id, department))

                elif choice == '4':
                    doctor_id = int(input("Enter Doctor's ID to remove: "))
                    print(admin.remove_doctor(doctor_id))

                elif choice == '5':
                    nurse_id = int(input("Enter Nurse's ID to remove: "))
                    print(admin.remove_nurse(nurse_id))
                    
                elif choice == '6':
                    support_staff_id = int(input("Enter Support Staff's ID to remove: "))
                    print(admin.remove_support_staff(support_staff_id))

                elif choice == '7':
                    staff = admin.get_all_staff()
                    print("Doctors: ", staff['doctors'])
                    print("Nurses: ", staff['nurses'])
                    print("Support Staffs: ", staff['support_staffs'])

                elif choice == '8':
                    doctor_id = int(input("Enter Doctor's ID: "))
                    day = input("Enter Day: ")
                    start_time = input("Enter Start Time: ")
                    end_time = input("Enter End Time: ")
                    print(admin.update_doctor_schedule(doctor_id, day, start_time, end_time))

                elif choice == '9':
                    nurse_id = int(input("Enter Nurse's ID: "))
                    day = input("Enter Day: ")
                    start_time = input("Enter Start Time: ")
                    end_time = input("Enter End Time: ")
                    print(admin.update_nurse_schedule(nurse_id, day, start_time, end_time))

                elif choice == '0':
                    break

                else:
                    print("Invalid choice. Please enter a number between 0 and 9.")
        elif choice == '9':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

    close_connection(conn)

if __name__ == '__main__':
    main()