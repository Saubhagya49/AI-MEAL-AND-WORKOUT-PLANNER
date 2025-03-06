import os
import sqlite3

# Define the database file path
DB_FILE = "user_data.db"

# Function to create the user database
def create_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Ensure the users table exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id TEXT PRIMARY KEY,  
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
def save_user_data(user_id, age, height, weight, goal, diet_type, equipment, experience_level):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Insert user data if not exists, otherwise update
    cursor.execute('''INSERT INTO users (user_id, age, height, weight, goal, diet_type, equipment, experience_level)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                      ON CONFLICT(user_id) 
                      DO UPDATE SET age=?, height=?, weight=?, goal=?, diet_type=?, equipment=?, experience_level=?''', 
                   (user_id, age, height, weight, goal, diet_type, equipment, experience_level,
                    age, height, weight, goal, diet_type, equipment, experience_level))
    
    conn.commit()
    conn.close()

# Function to fetch user data based on user_id
def get_user_data(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Make sure the table exists before querying
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if not cursor.fetchone():
        create_db()  # Create table if it doesn't exist

    cursor.execute("SELECT age, height, weight, goal, diet_type, equipment, experience_level FROM users WHERE user_id=?", (user_id,))
    user_data = cursor.fetchone()
    
    conn.close()
    return user_data  # Returns a tuple of user data

# Ensure database is created on import
create_db()
