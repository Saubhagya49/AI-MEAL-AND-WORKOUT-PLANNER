import os
import sqlite3

# Get the current directory of the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Correct the database path
db_path = os.path.join(BASE_DIR, "fitness_planner.db")  # Removed (1) to avoid issues

# Function to create the user database
def create_db():
    user_db_path = os.path.join(BASE_DIR, "user_data.db")
    conn = sqlite3.connect(user_db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (age INT, gender TEXT, weight INT, height INT, goal TEXT, 
                      diet_type TEXT, equipment TEXT, caloric_surplus TEXT)''')
    conn.commit()
    conn.close()

# Function to save user input into the database
def save_user_data(age, gender, weight, height, goal, diet_type, equipment):
    user_db_path = os.path.join(BASE_DIR, "user_data.db")
    conn = sqlite3.connect(user_db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                   (age, gender, weight, height, goal, diet_type, equipment))
    conn.commit()
    conn.close()

# Create the user database on startup
create_db()
