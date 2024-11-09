import streamlit as st
from pymongo import MongoClient
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_CLIENT"))  # replace with your MongoDB connection string
db = client["auth_app"]  # Create a database called auth_app
users_collection = db["users"]  # Create a collection called users

st.set_page_config(
    page_title="Sign Up",
    page_icon="✅",
    layout="centered",
)

# Helper function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Helper function to verify password
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password)

# Sign up function
def signup_user(username, password, first_name, last_name):
    if users_collection.find_one({"username": username}):
        return False  # Username already exists
    hashed_pw = hash_password(password)
    users_collection.insert_one(
        {"First Name": first_name, 
         "Last Name": last_name, 
         "username": username, 
         "password": hashed_pw, 
         "region": st.session_state.region,
            "dietary_preferences": st.session_state.dietary_preferences,
            "health_goal": st.session_state.health_goal,
            "meals_per_day": st.session_state.meals_per_day,
            "calorie_intake": st.session_state.calorie_intake,
            "allergies": st.session_state.allergies,
            "duration": st.session_state.duration,
            "user_question": st.session_state.user_question,
         })
    return True

st.title("Sign Up")
st.subheader("Create New Account", divider="orange")

first, last = st.columns(2)
first_name = first.text_input("First Name")
last_name = last.text_input("Last Name")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
if st.button("Sign Up"):
    if signup_user(username, password, first_name, last_name):
        st.success(f"Account created for {username}!")
    else:
        st.error("Username already exists. Please try a different one.")
