import sqlite3

# Define the database file path
DB_FILE = "user_data.db"

# ✅ Function to Create Database & Tables
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

    # ✅ Ensure meal_plans table exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS meal_plans (
                        user_id TEXT PRIMARY KEY,  
                        meal_plan TEXT,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )''')

    # ✅ Ensure workout_plans table exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS workout_plans (
                        user_id TEXT PRIMARY KEY,  
                        workout_plan TEXT,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )''')

    conn.commit()
    conn.close()

# ✅ Function to Save User Data
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

# ✅ Function to Save Meal Plan
def save_meal_plan(user_id, meal_plan):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Replace meal plan if user already has one
    cursor.execute('''INSERT INTO meal_plans (user_id, meal_plan)
                      VALUES (?, ?)
                      ON CONFLICT(user_id) 
                      DO UPDATE SET meal_plan=?''', 
                   (user_id, str(meal_plan), str(meal_plan)))

    conn.commit()
    conn.close()

# ✅ Function to Save Workout Plan
def save_workout_plan(user_id, workout_plan):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Replace workout plan if user already has one
    cursor.execute('''INSERT INTO workout_plans (user_id, workout_plan)
                      VALUES (?, ?)
                      ON CONFLICT(user_id) 
                      DO UPDATE SET workout_plan=?''', 
                   (user_id, str(workout_plan), str(workout_plan)))

    conn.commit()
    conn.close()

# ✅ Function to Retrieve User Data
def get_user_data(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT age, height, weight, goal, diet_type, equipment, experience_level FROM users WHERE user_id=?", (user_id,))
    user_data = cursor.fetchone()
    
    conn.close()
    return user_data  # Returns a tuple of user data

# ✅ Function to Retrieve Meal Plan
def get_meal_plan(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT meal_plan FROM meal_plans WHERE user_id=?", (user_id,))
    meal_plan = cursor.fetchone()
    conn.close()
    return meal_plan[0] if meal_plan else None

# ✅ Function to Retrieve Workout Plan
def get_workout_plan(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT workout_plan FROM workout_plans WHERE user_id=?", (user_id,))
    workout_plan = cursor.fetchone()
    conn.close()
    return workout_plan[0] if workout_plan else None

# Ensure database is created on import
create_db()
