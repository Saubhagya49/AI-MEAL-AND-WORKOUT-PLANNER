import os
import sqlite3

# Get the current directory of the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database path
user_db_path = os.path.join(BASE_DIR, "user_data.db")

# Function to create the user database
def create_db():
    conn = sqlite3.connect(user_db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        age INT, 
                        height INT, 
                        weight INT, 
                        goal TEXT, 
                        diet_type TEXT, 
                        equipment TEXT, 
                        experience_level TEXT
                    )''')
    conn.commit()
    conn.close()

# Function to save user input into the database
def save_user_data(age, height, weight, goal, diet_type, equipment, experience_level):
    conn = sqlite3.connect(user_db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (age, height, weight, goal, diet_type, equipment, experience_level))  # Now 7 values
    conn.commit()
    conn.close()
def get_user_data():
    user_db_path = os.path.join(BASE_DIR, "user_data.db")
    conn = sqlite3.connect(user_db_path)
    cursor = conn.cursor()

    # Fetch all user data
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()

    conn.close()
    return data  # Returns a list of tuples

# Create the user database on startup
create_db()
