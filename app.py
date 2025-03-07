import streamlit as st
import pandas as pd
from meal_and_workout_plan_generator import generate_meal_plan, generate_workout_routine
import database  # Import database functions

# 🎨 Streamlit Page Configuration
st.set_page_config(page_title="AI Diet & Workout Planner", layout="wide", page_icon="💪")

# 🏆 App Title & Introduction
st.title("🥗💪 AI-Based Diet & Workout Planner")
st.markdown("""
    Welcome to your **personalized AI-powered fitness assistant!**  
    🔥 Get a **custom meal & workout plan** based on your **goal, diet, and available equipment.**  
""")

# 📌 **User Input for New Plan & Saved Plan Access**
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Generate a New Plan")
    age = st.number_input("📅 Age", min_value=10, max_value=100, value=25)
    height = st.number_input("📏 Height (cm)", min_value=100, max_value=250, value=170)
    weight = st.number_input("⚖️ Weight (kg)", min_value=30, max_value=200, value=70)
    goal = st.selectbox("🎯 Fitness Goal", ["Maintain Weight", "Muscle Gain", "Bulk Up Fast"])
    diet_type = st.selectbox("🥗 Diet Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])

    # 🎛️ **Equipment Selection**
    equipment_map = {
        "💪 Bodyweight (No Equipment)": "body only",
        "🏋️ Dumbbells at Home": "dumbbell",
        "🏢 Full Gym Access": "Full Gym"
    }
    equipment = equipment_map[st.selectbox("🏋️ Equipment Available", list(equipment_map.keys()))]

    # 🎛️ **Experience Level Selection**
    level_map = {
        "🌱 Beginner (New to Fitness)": "beginner",
        "💪 Intermediate (Some Experience)": "intermediate",
        "🔥 Expert (Advanced Training)": "expert"
    }
    level = level_map[st.selectbox("📊 Experience Level", list(level_map.keys()))]

    # 🚀 **Generate Plan**
    if st.button("🚀 Generate My Plan"):
        st.session_state["meal_plan"] = generate_meal_plan(diet_type, goal, age, height, weight)
        st.session_state["workout_plan"] = generate_workout_routine(goal, equipment, level)
        st.session_state["show_plans"] = True  # Store flag to show generated plans

# ✅ **Step 1: Display Generated Plan (Persist after button clicks)**
if st.session_state.get("show_plans", False):
    st.subheader("🍽️ Personalized Meal Plan")
    st.markdown(st.session_state.get("meal_plan", ""), unsafe_allow_html=True)

    st.subheader("💪 Personalized Workout Plan")
    st.markdown(st.session_state.get("workout_plan", ""), unsafe_allow_html=True)

    # 💾 **Save Plan Button**
    if st.button("💾 Save This Plan"):
        st.session_state["show_save_options"] = True

# ✅ **Step 2: Ask What to Save**
if st.session_state.get("show_save_options", False):
    save_choice = st.radio("What do you want to save?", ["Meal Plan Only", "Workout Plan Only", "Save Both"])
    st.session_state["save_choice"] = save_choice  # Store in session state

    if save_choice:
        st.session_state["show_username_input"] = True

# ✅ **Step 3: Ask for Username**
if st.session_state.get("show_username_input", False):
    user_id = st.text_input("🔑 Enter Your Username or Email to Save Plan")

    if st.button("✅ Confirm Save"):
        if not user_id.strip():
            st.warning("⚠️ Please enter a valid username or email.")
        else:
            # Save plan based on user selection
            if st.session_state["save_choice"] == "Meal Plan Only":
                database.save_meal_plan(user_id, st.session_state["meal_plan"])
                st.success("🍽️ Meal Plan saved successfully!")
            elif st.session_state["save_choice"] == "Workout Plan Only":
                database.save_workout_plan(user_id, st.session_state["workout_plan"])
                st.success("💪 Workout Plan saved successfully!")
            elif st.session_state["save_choice"] == "Save Both":
                database.save_meal_plan(user_id, st.session_state["meal_plan"])
                database.save_workout_plan(user_id, st.session_state["workout_plan"])
                st.success("✅ Both Meal & Workout Plans saved successfully!")

with col2:
    st.subheader("📂 View My Saved Plans")

    if st.button("👀 View Saved Plans"):
        st.session_state["show_saved_input"] = True

    if st.session_state.get("show_saved_input", False):
        user_id = st.text_input("🔑 Enter Your Username or Email to Retrieve Plans")

        if st.button("📂 Retrieve My Plans"):
            user_data = database.get_user_data(user_id)
            if user_data:
                st.session_state["user_id"] = user_id  
                st.session_state["user_data"] = user_data
                st.session_state["view_saved"] = True  
            else:
                st.warning("⚠️ No data found for this user!")

    if st.session_state.get("view_saved", False):
        user_id = st.session_state["user_id"]
        user_data = st.session_state["user_data"]

        st.markdown(f"**🔑 Logged in as:** {user_id}")
        st.subheader("📊 Your Saved Data")
        st.markdown(f"""
        - **Age:** {user_data[0]}  
        - **Height:** {user_data[1]} cm  
        - **Weight:** {user_data[2]} kg  
        - **Goal:** {user_data[3]}  
        - **Diet:** {user_data[4]}  
        - **Equipment:** {user_data[5]}  
        - **Experience Level:** {user_data[6]}  
        """)

        saved_meal_plan = database.get_meal_plan(user_id)
        saved_workout_plan = database.get_workout_plan(user_id)

        if saved_meal_plan:
            st.subheader("🍽️ Your Saved Meal Plan")
            for meal, food_items in saved_meal_plan:
                st.markdown(f"🍽️ **{meal}:** {food_items}")

        if saved_workout_plan:
            st.subheader("💪 Your Saved Workout Plan")
            st.markdown(saved_workout_plan, unsafe_allow_html=True)
