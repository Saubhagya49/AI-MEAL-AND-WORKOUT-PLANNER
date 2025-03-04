import sqlite3

# Get the current directory of the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Correct the database path
db_path = os.path.join(BASE_DIR, "fitness_planner(1).db")

# Connect to SQLite
conn = sqlite3.connect(db_path)
def create_db():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (age INT, gender TEXT, weight INT, height INT, goal TEXT, diet_type TEXT, equipment TEXT, caloric_surplus TEXT)''')
    conn.commit()
    conn.close()

def save_user_data(age, gender, weight, height, goal, diet_type, equipment, caloric_surplus):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                   (age, gender, weight, height, goal, diet_type, equipment, caloric_surplus))
    conn.commit()
    conn.close()

create_db()
