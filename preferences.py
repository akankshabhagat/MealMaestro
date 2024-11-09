import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

# MongoDB connection setup
client = MongoClient(os.getenv("MONGO_CLIENT"))  # replace with your MongoDB connection string
db = client["auth_app"]  # Create a database called auth_app
users_collection = db["users"]  # Create a collection called users

# Configure the API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def update_preferences(username, region, dietary_preferences, health_goal, meals_per_day, calorie_intake, allergies, duration, user_question):
    users_collection.update_one(
        {"username": username},
        {
            "$set": {
                "region": region,
                "dietary_preferences": dietary_preferences,
                "health_goal": health_goal,
                "meals_per_day": meals_per_day,
                "calorie_intake": calorie_intake,
                "allergies": allergies,
                "duration": duration,
                "user_question": user_question,
            }
        }
    )

def image_url(prompt):
    width = 300
    height = 300
    seed = 5 # Each seed generates a new image variation
    model = 'turbo' # Using 'flux' as default if model is not provided

    image_url = f"https://pollinations.ai/p/{prompt}?width={width}&height={height}&seed={seed}&model={model}"
    st.image(image_url, use_column_width=True)


if st.session_state.login == False:
    st.error("You are not logged in. Please log in to access this page.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Meal Maestro",
    page_icon="🍲",
    layout="wide",
)

# Create two columns
col1, col2 = st.columns(2)

# Form for meal preferences in the left column
with col1:
    with st.form("preferences_form"):
        st.subheader("Meal Plan Preferences")

        # Region selection
        selected_region = st.selectbox("Select Region:", ["North Indian", "South Indian", "Mediterranean", "Asian", "American"])
        st.session_state.region = selected_region
        # Dietary restrictions
        dietary_preferences = st.multiselect(
            "Dietary Preferences:",
            ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Egg-Free", "Nut-Free"],
        )
        st.session_state.dietary_preferences = dietary_preferences
        # Health goal
        health_goal = st.radio("Health Goal:", ["Weight Loss", "Muscle Gain", "Maintain Weight"])
        st.session_state.health_goal = health_goal

        # Number of meals per day
        meals_per_day = st.selectbox("Number of Meals per Day:", [1, 2, 3, 4, 5, 6])
        st.session_state.meals_per_day = meals_per_day

        # Calorie intake
        calorie_intake = st.slider("Desired Daily Calorie Intake:", 1200, 3500, 2000)
        st.session_state.calorie_intake = calorie_intake

        # Allergies/Intolerances
        allergies = st.text_input("Allergies/Intolerances (e.g., nuts, gluten, dairy)")
        st.session_state.allergies = allergies

        # Plan duration
        duration = st.radio("Plan Duration:", ["Single Day", "One Week"])
        st.session_state.duration = duration

        # Additional customizations
        user_question = st.text_input("Additional Customizations:")
        st.session_state.user_question = user_question

        check = st.checkbox("With Recipes")

        # Generate button inside the form
        submit_button = st.form_submit_button("Generate")

        update_preferences(
            st.session_state.username,
            selected_region,
            dietary_preferences,
            health_goal,
            meals_per_day,
            calorie_intake,
            allergies,
            duration,
            user_question,
        )

    # Generate response if form is submitted
    if submit_button:
        # Clear history for a new request
        st.session_state.history = []

        # Set default user_question if empty
        if not user_question.strip():
            user_question = "Please generate a simple, short meal plan."

        # Format dietary preferences into a string for use in prompt
        dietary_preferences_str = ", ".join(dietary_preferences)

        if check:
            prompt = f"You are a diet planning bot. The user has these preferences: {dietary_preferences_str}, {health_goal}. They are from {selected_region}. Generate a {duration.lower()} meal plan with {meals_per_day} meals per day, aiming for {calorie_intake} calories, with each meal having a one-line description, and provide recipes for each meal."
        else:
            prompt = f"You are a diet planning bot. The user has these preferences: {dietary_preferences_str}, {health_goal}. They are from {selected_region}. Generate a {duration.lower()} meal plan with {meals_per_day} meals per day, aiming for {calorie_intake} calories, with each meal having a one-line description. Avoid tips and extra information."

        st.session_state.prompt = prompt
        # Initialize conversation history with updated preferences
        st.session_state.history.append(
            {"role": "model", "text": prompt}
        )

        # Generate response using the AI model
        chat = model.start_chat(
            history=[{"role": msg["role"], "parts": msg["text"]} for msg in st.session_state.history]
        )
        response = chat.send_message(user_question, stream=True)

        # Collect response text
        response_text = ""
        for chunk in response:
            response_text += chunk.text

        # Append the response to conversation history
        st.session_state.history.append({"role": "user", "text": user_question})
        st.session_state.history.append({"role": "model", "text": response_text})

# Display the response in the right column
with col2:
    if "history" in st.session_state and len(st.session_state.history) > 1:
        # Display the last model response
        last_response = st.session_state.history[-1]
        if last_response["role"] == "model":
            st.subheader("Meal Maestro's Response:")
            st.markdown(last_response["text"])