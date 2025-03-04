# -*- coding: utf-8 -*-
"""Meal & Workout Plan Generator"""

import os
import sqlite3
import pandas as pd
import random
import google.generativeai as genai

# ✅ Get the base directory of the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Use relative path for SQLite database
db_path = os.path.join(BASE_DIR, "fitness_planner.db")

# ✅ Load food data safely
try:
    conn = sqlite3.connect(db_path)
    df_food = pd.read_sql_query("SELECT * FROM food;", conn)
    conn.close()
except Exception as e:
    print(f"❌ Database Error: {e}")
    df_food = pd.DataFrame()  # Empty DataFrame to prevent errors

# ✅ Configure Gemini AI (Read API key from environment)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Use the latest Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

def generate_meal_plan(diet_type, calories):
    """Generate a meal plan using Gemini AI."""
    prompt = f"Suggest 3 high-protein {diet_type} meals under {calories} kcal."

    try:
        response = model.generate_content(prompt)
        ai_meals = response.text.strip().split("\n")
        return ai_meals
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return ["Error generating meal plan. Check API key & model availability."]

# ✅ Example usage
meal_plan = generate_meal_plan(diet_type="Vegetarian", calories=2500)

# ✅ Load workout data safely
try:
    conn = sqlite3.connect(db_path)
    df_workout = pd.read_sql_query("SELECT * FROM exercise;", conn)
    conn.close()
except Exception as e:
    print(f"❌ Database Error: {e}")
    df_workout = pd.DataFrame()

# ✅ Define muscle groups mapping
muscle_group_mapping = {
    "Chest": ["Chest"],
    "Back": ["Lats", "Middle Back", "Lower Back"],
    "Legs": ["Quadriceps", "Hamstrings", "Calves", "Glutes", "Adductors", "Abductors"],
    "Shoulders": ["Shoulders", "Traps"],
    "Arms": ["Biceps", "Triceps", "Forearms"],
    "Core": ["Abdominals"]
}

def generate_workout_routine(goal="Muscle Gain", equipment="Dumbbells", level="Intermediate"):
    """Generate a structured workout plan with error handling."""

    if df_workout.empty:
        return "❌ **Error:** No workout data found in the database!"

    df_workout.columns = df_workout.columns.str.lower()

    if "bodypart" not in df_workout.columns or "title" not in df_workout.columns:
        return "❌ **Error:** Missing required columns in dataset!"

    # ✅ Filter dataset based on user input
    filtered_workouts = df_workout[
        (df_workout["equipment"].str.contains(equipment, case=False, na=False)) &
        (df_workout["level"].str.contains(level, case=False, na=False))
    ]

    if filtered_workouts.empty:
        return f"❌ **Error:** No workouts found for {equipment}, {level} level."

    # ✅ Select exercises per muscle group
    workout_plan = {}
    for group, muscles in muscle_group_mapping.items():
        muscle_workouts = filtered_workouts[filtered_workouts["bodypart"].isin(muscles)]["title"]
        workout_plan[group] = muscle_workouts.sample(2).tolist() if not muscle_workouts.empty else ["❌ No exercises found"]

    # ✅ Format workout plan
    formatted_workout_plan = "\n\n".join(
        [f"### **{muscle}**\n" + "\n".join([f"- {exercise}" for exercise in exercises])
         for muscle, exercises in workout_plan.items()]
    )

    # ✅ AI-enhanced structured workout plan
    prompt = f"""
    Given these exercises: {workout_plan},
    Create a structured **5-day workout plan** for {goal}.
    """
    try:
        ai_response = model.generate_content(prompt)
    except Exception as e:
        ai_response = f"❌ AI Error: {e}"

    return f"""
## 🏋️ Personalized Workout Routine

{formatted_workout_plan}

---

## 📋 AI-Generated 5-Day Workout Plan
{ai_response.text if isinstance(ai_response, object) else ai_response}
"""

# ✅ Example usage
result = generate_workout_routine("Muscle Gain", "Dumbbells", "Intermediate")
print(result)
