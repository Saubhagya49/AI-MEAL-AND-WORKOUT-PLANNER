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

# 📌 **Option to View Saved Plans**
if st.button("📂 View My Saved Plans"):
    user_id = st.text_input("🔑 Enter Your Username or Email to View Plans")
    
    if user_id:
        user_data = database.get_user_data(user_id)
        
        if user_data:
            st.session_state["user_id"] = user_id  # Store for later use
            st.session_state["user_data"] = user_data
            st.session_state["view_saved"] = True  # Enable full screen mode
        else:
            st.warning("⚠️ No data found for this user!")

# 🚀 **Show Full Screen After Login**
if "view_saved" in st.session_state and st.session_state["view_saved"]:
    user_id = st.session_state["user_id"]
    user_data = st.session_state["user_data"]

    st.header(f"🔑 Logged in as {user_id}")
    
    # 📊 Show saved details
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

    # 🏋️ Show existing saved plans
    saved_meal_plan = database.get_meal_plan(user_id)
    saved_workout_plan = database.get_workout_plan(user_id)

    if saved_meal_plan:
        st.subheader("🍽️ Your Saved Meal Plan")
        for meal, food_items in saved_meal_plan:
            st.markdown(f"🍽️ **{meal}:** {food_items}")

    if saved_workout_plan:
        st.subheader("💪 Your Saved Workout Plan")
        st.markdown(saved_workout_plan, unsafe_allow_html=True)

    # 📥 **Option to Generate a New Plan**
    if st.button("🚀 Generate New Plan"):
        st.session_state["generate_plan"] = True

# ✅ **Generate New Plan**
if "generate_plan" in st.session_state and st.session_state["generate_plan"]:
    with st.form("user_input"):
        st.subheader("📝 Enter Your Details")
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("📅 Age", min_value=10, max_value=100, value=user_data[0])
            height = st.number_input("📏 Height (cm)", min_value=100, max_value=250, value=user_data[1])
            weight = st.number_input("⚖️ Weight (kg)", min_value=30, max_value=200, value=user_data[2])

        with col2:
            goal = st.selectbox("🎯 Fitness Goal", ["Maintain Weight", "Muscle Gain", "Bulk Up Fast"], 
                                index=["Maintain Weight", "Muscle Gain", "Bulk Up Fast"].index(user_data[3]))
            diet_type = st.selectbox("🥗 Diet Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"], 
                                     index=["Vegetarian", "Non-Vegetarian", "Vegan"].index(user_data[4]))
            equipment = st.selectbox("🏋️ Equipment Available", ["Bodyweight Only", "Dumbbells", "Full Gym"], 
                                     index=["Bodyweight Only", "Dumbbells", "Full Gym"].index(user_data[5]))

        level = st.selectbox("📊 Experience Level", ["Beginner", "Intermediate", "Expert"], 
                             index=["Beginner", "Intermediate", "Expert"].index(user_data[6]))

        submitted = st.form_submit_button("🚀 Generate My Plan")

    # **Generate Plans**
    if submitted:
        meal_plan = generate_meal_plan(diet_type, goal, age, height, weight)
        workout_plan = generate_workout_routine(goal, equipment, level)

        st.success("✅ Your plan has been successfully generated!")

        # 📊 **Display Meal Plan**
        st.header("🍽️ Personalized Meal Plan")
        if isinstance(meal_plan, list) and all(isinstance(meal, (list, tuple)) and len(meal) == 2 for meal in meal_plan):
            for meal, food_items in meal_plan:
                st.markdown(f"🍽️ **{meal}:** {food_items}")
        else:
            st.warning("⚠️ No meal plan generated. Try changing your preferences.")

        # 🏋️ **Display Workout Plan**
        st.header("💪 Personalized Workout Plan")
        if isinstance(workout_plan, str):
            st.markdown(workout_plan, unsafe_allow_html=True)
        else:
            st.error("⚠️ Error: Workout plan is not in the expected format!")

        # 🔘 **Ask if the user wants to save**
        st.subheader("💾 Save Your Plan?")
        save_choice = st.radio("Choose what you want to save:", 
                               ["Don't Save", "Meal Plan Only", "Workout Plan Only", "Save Both"])

        if st.button("💾 Confirm Save"):
            if save_choice == "Meal Plan Only":
                database.save_meal_plan(user_id, meal_plan)
                st.success("🍽️ Meal Plan saved successfully!")
            elif save_choice == "Workout Plan Only":
                database.save_workout_plan(user_id, workout_plan)
                st.success("💪 Workout Plan saved successfully!")
            elif save_choice == "Save Both":
                database.save_meal_plan(user_id, meal_plan)
                database.save_workout_plan(user_id, workout_plan)
                st.success("✅ Both Meal & Workout Plans saved successfully!")

