import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Page configuration
st.set_page_config(
    page_title="Meal Maestro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Create two columns
col1, col2 = st.columns(2)

# Form for meal preferences in the left column
with col1:
    with st.form("preferences_form"):
        st.subheader("Meal Plan Preferences")

        # Region selection
        selected_region = st.selectbox("Select Region:", ["North Indian", "South Indian", "Mediterranean", "Asian", "American"])

        # Dietary restrictions
        dietary_preferences = st.multiselect(
            "Dietary Preferences:",
            ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free"]
        )

        # Health goal
        health_goal = st.radio("Health Goal:", ["Weight Loss", "Muscle Gain", "Maintain Weight"])

        # Number of meals per day
        meals_per_day = st.selectbox("Number of Meals per Day:", [1, 2, 3, 4, 5, 6])

        # Calorie intake
        calorie_intake = st.slider("Desired Daily Calorie Intake:", 1200, 3500, 2000)

        # Allergies/Intolerances
        allergies = st.text_input("Allergies/Intolerances (e.g., nuts, gluten, dairy)")

        # Plan duration
        duration = st.radio("Plan Duration:", ["Single Day", "One Week"])

        # Additional customizations
        user_question = st.text_input("Additional Customizations:")

        # Generate button inside the form
        submit_button = st.form_submit_button("Generate")

    # Generate response if form is submitted
    if submit_button:
        # Clear history for a new request
        st.session_state.history = []

        # Set default user_question if empty
        if not user_question.strip():
            user_question = "Please generate a simple, short meal plan."

        # Format dietary preferences into a string for use in prompt
        dietary_preferences_str = ", ".join(dietary_preferences)

        # Initialize conversation history with updated preferences
        st.session_state.history.append(
            {"role": "model", "text": f"You are a diet planning bot. The user has these preferences: {dietary_preferences_str}, {health_goal}. They are from {selected_region}. Generate a {duration.lower()} meal plan with {meals_per_day} meals per day, aiming for {calorie_intake} calories, with each meal having a one-line description. Avoid tips and extra information."}
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
            st.write(last_response["text"])
