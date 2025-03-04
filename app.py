import streamlit as st
import pandas as pd
from meal_and_workout_plan_generator import generate_meal_plan  
from meal_and_workout_plan_generator import generate_workout_routine  
import database  # Import database logic




st.set_page_config(page_title="AI Diet & Workout Planner", layout="wide")

st.title("🥗💪 AI-Based Diet & Workout Planner")
st.write("🚀 App Started!")  # Debugging Step
# 🎯 User Input Form
with st.form("user_input"):
    age = st.number_input("Age", min_value=10, max_value=100, value=25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
    height = st.number_input("Height (cm)", min_value=100, max_value=250, value=175)
    goal = st.selectbox("Goal", ["Maintain Weight", "Muscle Gain", "Bulk Up Fast"])
    diet_type = st.selectbox("Diet Preference", ["Veg", "Non-Veg", "Vegan"])
    equipment = st.selectbox("Equipment", ["Bodyweight", "Dumbbells", "Full Gym"])
    caloric_surplus = st.selectbox("Caloric Surplus", ["Slow", "Moderate", "Aggressive"])
    
    submitted = st.form_submit_button("🚀 Generate Plan")

if submitted:
    meal_plan = generate_meal_plan(goal, diet_type, caloric_surplus)  # Get meal plan
    workout_plan = generate_workout_routine(goal, equipment)  # Get workout plan

    # Display results beautifully
    st.header("🍽️ Personalized Meal Plan")
    st.markdown(meal_plan, unsafe_allow_html=True)

    st.header("💪 Personalized Workout Plan")
    st.markdown(workout_plan, unsafe_allow_html=True)

    # Save user data to database
    database.save_user_data(age, gender, weight, height, goal, diet_type, equipment, caloric_surplus)
