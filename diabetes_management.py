import sqlite3
from datetime import datetime

# Database connection and cursor
conn = sqlite3.connect("diabetes_management.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS blood_sugar(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    reading REAL,
    reading_date TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS insulin_dosage(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    dosage REAL,
    dosage_time TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    appointment_date TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS nutrition_goals(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    goal TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

# Create table for logging user actions
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_actions (
    id INTEGER PRIMARY KEY,
    action_type TEXT,
    timestamp TEXT,
    details TEXT
)
""")

# Commit changes and close the connection
conn.commit()


class BloodSugar:
    def __init__(self, user_id, reading=None):
        self.user_id = user_id
        self.reading = reading

    def add_reading(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            cursor.execute("""INSERT INTO blood_sugar(user_id, reading, reading_date) VALUES(?, ?, ?)""",
                           (self.user_id, self.reading, current_time))
            conn.commit()
            print("Blood sugar reading added successfully!")
            log_action("Add Blood Sugar Reading", f"Reading: {self.reading}")

        except sqlite3.Error as error:
            print(f"Error adding blood sugar reading: {error}")

    @staticmethod
    def get_all_readings(user_id):
        try:
            cursor.execute("SELECT * FROM blood_sugar WHERE user_id = ?", (user_id,))
            readings = cursor.fetchall()
            return readings
        except sqlite3.Error as error:
            print(f"Error fetching blood sugar readings: {error}")


class InsulinDosage:
    def __init__(self, user_id, dosage=None):
        self.user_id = user_id
        self.dosage = dosage

    def add_dosage(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            cursor.execute("""INSERT INTO insulin_dosage(user_id, dosage, dosage_time) VALUES(?, ?, ?)""",
                           (self.user_id, self.dosage, current_time))
            conn.commit()
            print("Insulin dosage added successfully!")
            log_action("Add Insulin Dosage", f"Dosage: {self.dosage}")

        except sqlite3.Error as error:
            print(f"Error adding insulin dosage: {error}")

    @staticmethod
    def get_all_dosages(user_id):
        try:
            cursor.execute("SELECT * FROM insulin_dosage WHERE user_id = ?", (user_id,))
            dosages = cursor.fetchall()
            return dosages
        except sqlite3.Error as error:
            print(f"Error fetching insulin dosages: {error}")


class Appointment:
    def __init__(self, user_id, appointment_date=None):
        self.user_id = user_id
        self.appointment_date = appointment_date

    def book_appointment(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            cursor.execute("""INSERT INTO appointments(user_id, appointment_date) VALUES(?, ?)""",
                           (self.user_id, current_time))
            conn.commit()
            print("Appointment booked successfully!")
            log_action("Book Appointment")

        except sqlite3.Error as error:
            print(f"Error booking appointment: {error}")

    @staticmethod
    def get_all_appointments(user_id):
        try:
            cursor.execute("SELECT * FROM appointments WHERE user_id = ?", (user_id,))
            appointments = cursor.fetchall()
            return appointments
        except sqlite3.Error as error:
            print(f"Error fetching appointments: {error}")


class NutritionGoal:
    def __init__(self, user_id, goal=None):
        self.user_id = user_id
        self.goal = goal

    def set_goal(self):
        try:
            cursor.execute("""INSERT INTO nutrition_goals(user_id, goal) VALUES(?, ?)""",
                           (self.user_id, self.goal))
            conn.commit()
            print("Nutrition goal set successfully!")
            log_action("Set Nutrition Goal", f"Goal: {self.goal}")

        except sqlite3.Error as error:
            print(f"Error setting nutrition goal: {error}")

    @staticmethod
    def get_all_goals(user_id):
        try:
            cursor.execute("SELECT * FROM nutrition_goals WHERE user_id = ?", (user_id,))
            goals = cursor.fetchall()
            return goals
        except sqlite3.Error as error:
            print(f"Error fetching nutrition goals: {error}")


def register_user(username, password):
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password))
    conn.commit()


def login_user(username, password):
    cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if row and password == row[1]:
        return row[0]  # Return user ID if login successful
    else:
        return None  # Return None if login failed


def log_action(action_type, details=None):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute("""INSERT INTO user_actions(action_type, timestamp, details) VALUES(?, ?, ?)""",
                       (action_type, current_time, details))
        conn.commit()
        print("Action logged successfully!")

    except sqlite3.Error as error:
        print(f"Error logging action: {error}")


def main():
    while True:
        print("\n=== Ayalink - Diabetes Management App ===")
        print("1. Register")
        print("2. Login")
        print("3. Add Blood Sugar Reading")
        print("4. Add Insulin Dosage")
        print("5. Book Appointment")
        print("6. Set Nutrition Goal")
        print("7. View All Blood Sugar Readings")
        print("8. View All Insulin Dosages")
        print("9. View All Appointments")
        print("10. View All Nutrition Goals")
        print("11. View All Activity Logs")
        print("12. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user(username, password)
            print
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            user_id = login_user(username, password)
            if user_id:
                print(f"Login successful! Welcome, {username}!")
                while True:
                    print("\n=== Dashboard ===")
                    print("1. Add Blood Sugar Reading")
                    print("2. Add Insulin Dosage")
                    print("3. Book Appointment")
                    print("4. Set Nutrition Goal")
                    print("5. View All Blood Sugar Readings")
                    print("6. View All Insulin Dosages")
                    print("7. View All Appointments")
                    print("8. View All Nutrition Goals")
                    print("9. View All Activity Logs")
                    print("10. Logout")

                    user_choice = input("Enter your choice: ")
                    if user_choice == "1":
                        reading = float(input("Enter blood sugar reading: "))
                        blood_sugar = BloodSugar(user_id, reading)
                        blood_sugar.add_reading()
                    elif user_choice == "2":
                        dosage = float(input("Enter insulin dosage: "))
                        insulin_dosage = InsulinDosage(user_id, dosage)
                        insulin_dosage.add_dosage()
                    elif user_choice == "3":
                        appointment = Appointment(user_id)
                        appointment.book_appointment()
                    elif user_choice == "4":
                        goal = input("Enter nutrition goal: ")
                        nutrition_goal = NutritionGoal(user_id, goal)
                        nutrition_goal.set_goal()
                    elif user_choice == "5":
                        readings = BloodSugar.get_all_readings(user_id)
                        print("All Blood Sugar Readings:")
                        for reading in readings:
                            print(reading)
                    elif user_choice == "6":
                        dosages = InsulinDosage.get_all_dosages(user_id)
                        print("All Insulin Dosages:")
                        for dosage in dosages:
                            print(dosage)
                    elif user_choice == "7":
                        appointments = Appointment.get_all_appointments(user_id)
                        print("All Appointments:")
                        for appointment in appointments:
                            print(appointment)
                    elif user_choice == "8":
                        goals = NutritionGoal.get_all_goals(user_id)
                        print("All Nutrition Goals:")
                        for goal in goals:
                            print(goal)
                    elif user_choice == "9":
                        logs = cursor.execute("SELECT * FROM user_actions").fetchall()
                        print("All Activity Logs:")
                        for log in logs:
                            print(log)
                    elif user_choice == "10":
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice!")

            else:
                print("Login failed! Invalid username or password.")
        elif choice == "12":
            print("Exiting the program...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
    conn.close()
