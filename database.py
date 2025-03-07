import sqlite3

# Define the database file path
DB_FILE = "user_data.db"

# ✅ Create Database & Tables
def create_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Users Table
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

    # Meal Plans Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS meal_plans (
                        user_id TEXT PRIMARY KEY,  
                        meal_plan TEXT,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )''')

    # Workout Plans Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS workout_plans (
                        user_id TEXT PRIMARY KEY,  
                        workout_plan TEXT,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )''')

    conn.commit()
    conn.close()

# ✅ Save User Data
def save_user_data(user_id, age, height, weight, goal, diet_type, equipment, experience_level):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO users (user_id, age, height, weight, goal, diet_type, equipment, experience_level)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                      ON CONFLICT(user_id) 
                      DO UPDATE SET age=?, height=?, weight=?, goal=?, diet_type=?, equipment=?, experience_level=?''', 
                   (user_id, age, height, weight, goal, diet_type, equipment, experience_level,
                    age, height, weight, goal, diet_type, equipment, experience_level))
    
    conn.commit()
    conn.close()

# ✅ Save Meal Plan (as a string)
def save_meal_plan(user_id, meal_plan):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Ensure user exists before saving meal plan
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))

    cursor.execute('''INSERT INTO meal_plans (user_id, meal_plan)
                      VALUES (?, ?)
                      ON CONFLICT(user_id) 
                      DO UPDATE SET meal_plan=?''', 
                   (user_id, meal_plan, meal_plan))

    conn.commit()
    conn.close()

# ✅ Save Workout Plan (as a string)
def save_workout_plan(user_id, workout_plan):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Ensure user exists before saving workout plan
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))

    cursor.execute('''INSERT INTO workout_plans (user_id, workout_plan)
                      VALUES (?, ?)
                      ON CONFLICT(user_id) 
                      DO UPDATE SET workout_plan=?''', 
                   (user_id, workout_plan, workout_plan))

    conn.commit()
    conn.close()

# ✅ Retrieve User Data
def get_user_data(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT age, height, weight, goal, diet_type, equipment, experience_level FROM users WHERE user_id=?", (user_id,))
    user_data = cursor.fetchone()
    
    conn.close()
    return user_data  # Returns a tuple (age, height, weight, ...)

# ✅ Retrieve Meal Plan (as string)
def get_meal_plan(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT meal_plan FROM meal_plans WHERE user_id=?", (user_id,))
    meal_plan = cursor.fetchone()
    conn.close()
    return meal_plan[0] if meal_plan else None

# ✅ Retrieve Workout Plan (as string)
def get_workout_plan(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT workout_plan FROM workout_plans WHERE user_id=?", (user_id,))
    workout_plan = cursor.fetchone()
    conn.close()
    return workout_plan[0] if workout_plan else None

# Ensure database is created on import
create_db()
