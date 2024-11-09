import streamlit as st
import requests
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
# MongoDB connection setup
client = MongoClient(os.getenv("MONGO_CLIENT"))  # replace with your MongoDB connection string
db = client["auth_app"]  # Create a database called auth_app
users_collection = db["users"]  # Create a collection called users

pages = {
    "Home": [st.Page("home.py", title="Home")],
    "Your account": [
        st.Page("login.py", title="Log in"),
        st.Page("signup.py", title="Sign up"),
        st.Page("preferences.py", title="Meal preferences"),
    ],
    "Resources": [
        st.Page("image.py", title="Image"),
        st.Page("recipe.py", title="Recipe"), 
    ],
}

pg = st.navigation(pages)
pg.run()

if "login" not in st.session_state:
    st.session_state.login = False

if "username" not in st.session_state:
    st.session_state.username = None

if "calorie" not in st.session_state:
      st.session_state.calorie = 0

if "region" not in st.session_state:
    st.session_state.region = "North Indian"

if "dietary_preferences" not in st.session_state:
    st.session_state.dietary_preferences = []

if "health_goal" not in st.session_state:
    st.session_state.health_goal = "Weight Loss"

if "meals_per_day" not in st.session_state:
    st.session_state.meals_per_day = 1

if "calorie_intake" not in st.session_state:
    st.session_state.calorie_intake = 2000

if "allergies" not in st.session_state:
    st.session_state.allergies = ""

if "duration" not in st.session_state:
    st.session_state.duration = "Single Day"

if "user_question" not in st.session_state:
    st.session_state.user_question = ""

if "prompt" not in st.session_state:
    st.session_state.prompt = ""

st.sidebar.title("Calorie Counter")
st.sidebar.write("Enter the food item you want to search for:")
c = st.sidebar.container()
query = c.text_input("Enter food item")
if c.button("Search"):
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    response = requests.get(api_url + query, headers={'X-Api-Key': os.getenv("NINJA_API_KEY")})
    if response.status_code == requests.codes.ok:
        output = response.json()
        st.session_state.calorie += float(output['items'][0]['calories'])
        c.write(f"Calories in {query} : {output['items'][0]['calories']}")
    else:
        c.write("Error:", response.status_code, response.text)

if c.button("Reset"):
    st.session_state.calorie = 0

st.sidebar.metric("Total Calories", value = st.session_state.calorie)