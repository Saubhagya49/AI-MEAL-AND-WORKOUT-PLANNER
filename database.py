import os
import sqlite3



# Function to create the user database
def create_db():
    user_db_path = os.path.join(BASE_DIR, "user_data.db")
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
    user_db_path = os.path.join(BASE_DIR, "user_data.db")
    conn = sqlite3.connect(user_db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (age, height, weight, goal, diet_type, equipment, experience_level))  # Now 7 values
    conn.commit()
    conn.close()

# Create the user database on startup
create_db()
