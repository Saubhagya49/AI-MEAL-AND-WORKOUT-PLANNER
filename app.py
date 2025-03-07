import streamlit as st
import pandas as pd
from meal_and_workout_plan_generator import generate_meal_plan, generate_workout_routine
import database  # Import database functions

st.set_page_config(page_title="AI Diet & Workout Planner", layout="wide", page_icon="💪")

st.title("🥗💪 AI-Based Diet & Workout Planner")
st.markdown("""
    Welcome to your **personalized AI-powered fitness assistant!**  
    🔥 Get a **custom meal & workout plan** based on your **goal, diet, and available equipment.**  
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Generate a New Plan")
    age = st.number_input("📅 Age", min_value=10, max_value=100, value=25)
    height = st.number_input("📏 Height (cm)", min_value=100, max_value=250, value=170)
    weight = st.number_input("⚖️ Weight (kg)", min_value=30, max_value=200, value=70)
    goal = st.selectbox("🎯 Fitness Goal", ["Maintain Weight", "Muscle Gain", "Bulk Up Fast"])
    diet_type = st.selectbox("🥗 Diet Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])

    equipment_map = {
        "💪 Bodyweight (No Equipment)": "body only",
        "🏋️ Dumbbells at Home": "dumbbell",
        "🏢 Full Gym Access": "Full Gym"
    }
    equipment = equipment_map[st.selectbox("🏋️ Equipment Available", list(equipment_map.keys()))]

    level_map = {
        "🌱 Beginner (New to Fitness)": "beginner",
        "💪 Intermediate (Some Experience)": "intermediate",
        "🔥 Expert (Advanced Training)": "expert"
    }
    level = level_map[st.selectbox("📊 Experience Level", list(level_map.keys()))]

    if st.button("🚀 Generate My Plan"):
        meal_plan = generate_meal_plan(diet_type, goal, age, height, weight)
        workout_plan = generate_workout_routine(goal, equipment, level)

        st.session_state["meal_plan"] = meal_plan
        st.session_state["workout_plan"] = workout_plan
        st.session_state["show_plans"] = True

if st.session_state.get("show_plans", False):
    st.subheader("🍽️ Personalized Meal Plan")
    st.markdown(st.session_state["meal_plan"], unsafe_allow_html=True)

    st.subheader("💪 Personalized Workout Plan")
    st.markdown(st.session_state["workout_plan"], unsafe_allow_html=True)

    if st.button("💾 Save This Plan"):
        st.session_state["show_save_options"] = True

if st.session_state.get("show_save_options", False):
    save_choice = st.radio("What do you want to save?", ["Meal Plan Only", "Workout Plan Only", "Save Both"])
    st.session_state["save_choice"] = save_choice

if st.session_state.get("save_choice"):
    user_id = st.text_input("🔑 Enter Your Username or Email to Save Plan")

    if st.button("✅ Confirm Save"):
        if not user_id.strip():
            st.warning("⚠️ Please enter a valid username or email.")
        else:
            database.save_user_data(user_id, age, height, weight, goal, diet_type, equipment, level)
            if st.session_state["save_choice"] == "Meal Plan Only":
                database.save_meal_plan(user_id, st.session_state["meal_plan"])
            elif st.session_state["save_choice"] == "Workout Plan Only":
                database.save_workout_plan(user_id, st.session_state["workout_plan"])
            else:
                database.save_meal_plan(user_id, st.session_state["meal_plan"])
                database.save_workout_plan(user_id, st.session_state["workout_plan"])
            st.success("✅ Plan saved successfully!")

with col2:
    st.subheader("📂 View My Saved Plans")
    user_id = st.text_input("🔑 Enter Your Username or Email to Retrieve Plans")

    if st.button("📂 Retrieve My Plans"):
        meal_plan = database.get_meal_plan(user_id)
        workout_plan = database.get_workout_plan(user_id)

        if meal_plan or workout_plan:
            st.subheader("🍽️ Saved Meal Plan")
            st.markdown(meal_plan or "No meal plan found.")

            st.subheader("💪 Saved Workout Plan")
            st.markdown(workout_plan or "No workout plan found.")
        else:
            st.warning("⚠️ No data found for this user!")
