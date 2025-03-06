import streamlit as st
import pandas as pd
from meal_and_workout_plan_generator import generate_meal_plan, generate_workout_routine
import database  # Import database functions

# 🎨 Streamlit Page Configuration
st.set_page_config(page_title="AI Diet & Workout Planner", layout="wide")

# 🏆 App Title & Introduction
st.title("🥗💪 AI Diet & Workout Planner")
st.markdown(
    """
    Welcome to your **AI-powered fitness assistant!** 🎯
    - 📌 Get a **personalized meal & workout plan** based on your **goal, diet, and available equipment**.
    - 📈 Track your progress and optimize your fitness journey.
    Let's get started! 🚀
    """,
    unsafe_allow_html=True,
)

# 📥 **User Login Section**
st.sidebar.header("🔑 User Login")
user_id = st.sidebar.text_input("Enter Your Unique ID (Email or Username)", key="user_id")

if user_id:
    user_data = database.get_user_data(user_id)

    # 📌 **User Input Form**
    with st.form("user_input_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("📅 Age", min_value=10, max_value=100, value=user_data[0] if user_data else 25)
            height = st.number_input("📏 Height (cm)", min_value=100, max_value=250, value=user_data[1] if user_data else 175)
            weight = st.number_input("⚖️ Weight (kg)", min_value=30, max_value=200, value=user_data[2] if user_data else 70)
        
        with col2:
            goal = st.selectbox("🎯 Fitness Goal", ["Maintain Weight", "Muscle Gain", "Bulk Up Fast"], 
                                index=["Maintain Weight", "Muscle Gain", "Bulk Up Fast"].index(user_data[3]) if user_data else 0)
            diet_type = st.selectbox("🥗 Diet Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"], 
                                     index=["Vegetarian", "Non-Vegetarian", "Vegan"].index(user_data[4]) if user_data else 0)
            equipment = st.selectbox("🏋️ Equipment Available", ["Body Only", "Dumbbells", "Full Gym"], 
                                     index=["Body Only", "Dumbbells", "Full Gym"].index(user_data[5]) if user_data else 0)
            level = st.selectbox("📊 Experience Level", ["Beginner", "Intermediate", "Expert"], 
                                 index=["Beginner", "Intermediate", "Expert"].index(user_data[6]) if user_data else 0)
        
        submitted = st.form_submit_button("🚀 Generate My Plan")
    
    # ✅ **Generate Plans on Submission**
    if submitted:
        meal_plan = generate_meal_plan(diet_type, goal, age, height, weight)
        workout_plan = generate_workout_routine(goal, equipment, level)

        # 📊 **Meal Plan Section**
        st.header("🍽️ Your Personalized Meal Plan")
        st.table(pd.DataFrame(meal_plan, columns=["Meal", "Food Items", "Calories", "Protein (g)"]))

        # 🏋️ **Workout Plan Section**
        st.header("💪 Your Personalized Workout Plan")
        st.markdown(workout_plan, unsafe_allow_html=True)

        # 💾 Save user data
        database.save_user_data(user_id, age, height, weight, goal, diet_type, equipment, level)
        st.success("✅ Your plan has been successfully generated & saved!")

    # 📊 **Display Saved User Data**
    st.sidebar.subheader("📁 Your Saved Data")
    if user_data:
        st.sidebar.markdown(
            f"""
            - **Age:** {user_data[0]}
            - **Height:** {user_data[1]} cm
            - **Weight:** {user_data[2]} kg
            - **Goal:** {user_data[3]}
            - **Diet:** {user_data[4]}
            - **Equipment:** {user_data[5]}
            - **Experience Level:** {user_data[6]}
            """
        )
    else:
        st.sidebar.write("No data found. Please enter your details above.")
