import streamlit as st
from pymongo import MongoClient
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection setup
client = MongoClient(os.getenv("MONGO_CLIENT"))  # replace with your MongoDB connection string
db = client["auth_app"]  # Create a database called auth_app
users_collection = db["users"]  # Create a collection called users

def get_data(username, item):
    data = users_collection.distinct(item, {"username": username})

# Helper function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Helper function to verify password
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password)

# Login function
def login_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and verify_password(user["password"], password):
        return True
    return False

st.set_page_config(
    page_title="Login",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.subheader("Login Section", divider="orange")

login, logout = st.columns(2)

if logout.button("Logout"):
    st.session_state.login = False
    st.session_state.username = None
    st.success("You have been logged out.")
    st.write("Please log in again to access the app.")
    st.stop()

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if login.button("Login"):
    if login_user(username, password):
        st.session_state.username = username
        st.session_state.login = True
        st.session_state.region = get_data(username, "region")
        st.session_state.dietary_preferences = get_data(username, "dietary_preferences")
        st.session_state.health_goal = get_data(username, "health_goal")
        st.session_state.meals_per_day = get_data(username, "meals_per_day")
        st.session_state.calorie_intake = get_data(username, "calorie_intake")
        st.session_state.allergies = get_data(username, "allergies")
        st.session_state.duration = get_data(username, "duration")
        st.session_state.user_question = get_data(username, "user_question")
        st.success(f"Welcome {username}!")
        st.write("You are logged in.")
        st.switch_page("home.py")
    else:
        st.error("Invalid username or password")
        st.write("Please try again.")

