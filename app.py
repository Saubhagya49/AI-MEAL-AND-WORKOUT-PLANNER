import streamlit as st
import pandas as pd
from meal_and_workout_plan_generator import generate_meal_plan, generate_workout_routine
import database  # Import database functions

# 🎨 Streamlit Page Configuration
st.set_page_config(page_title="AI Diet & Workout Planner", layout="wide")

# 🏆 App Title & Introduction
st.title("🥗💪 AI-Based Diet & Workout Planner")
st.markdown("""
    Welcome to your **personalized AI-powered fitness assistant!**  
    🔥 Get a **custom meal & workout plan** tailored to your **goal, diet, and equipment.**  
    Let's get started! 🚀
""")

# 📥 **User Input Form**
with st.form("user_input"):
    age = st.number_input("📅 Age", min_value=10, max_value=100, value=25)
    gender = st.selectbox("⚧️ Gender", ["Male", "Female", "Other"])
    weight = st.number_input("⚖️ Weight (kg)", min_value=30, max_value=200, value=70)
    height = st.number_input("📏 Height (cm)", min_value=100, max_value=250, value=175)
    goal = st.selectbox("🎯 Fitness Goal", ["Maintain Weight", "Muscle Gain", "Bulk Up Fast"])
    diet_type = st.selectbox("🥗 Diet Preference", ["Veg", "Non-Veg", "Vegan"])
    equipment = st.selectbox("🏋️ Equipment Available", ["Bodyweight", "Dumbbells", "Full Gym"])
    caloric_surplus = st.selectbox("🔥 Caloric Surplus Preference", ["Slow", "Moderate", "Aggressive"])

    # 🎛️ Submit Button
    submitted = st.form_submit_button("🚀 Generate My Plan")

# ✅ **Generate Plans on Submission**
if submitted:
    # 🥗 Generate Meal Plan
    meal_plan = generate_meal_plan(diet_type, goal, age, height, weight)
    
    # 🏋️ Generate Workout Plan
    workout_plan = generate_workout_routine(goal, equipment, "intermediate")

    # 📊 Display **Meal Plan**
    st.header("🍽️ Personalized Meal Plan")
    if isinstance(meal_plan, list):  # If meal plan is a list of meals
        for meal in meal_plan:
            st.write(f"✅ {meal}")
    else:
        st.markdown(meal_plan, unsafe_allow_html=True)

    # 🏋️ Display **Workout Plan**
    st.header("💪 Personalized Workout Plan")
    st.markdown(workout_plan, unsafe_allow_html=True)

    # 💾 Save user data to database
    database.save_user_data(age, gender, weight, height, goal, diet_type, equipment, caloric_surplus)

    st.success("✅ Your plan has been successfully generated & saved!")

