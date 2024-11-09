import streamlit as st
import os
import google.generativeai as genai


st.set_page_config(
    page_title="Meal Maestro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel("gemini-1.5-flash")

region ="north Indian"
dietary_restrictions =" Vegetarian, vegan, gluten-free,"


if "history" not in st.session_state:
    
    st.session_state.history = [
        {"role": "model", "text": f"you are diet planning bot the user has these restrictions:{dietary_restrictions}  he is from {region} *"},
    #    {"role": "model", "text": f"hELP ME WILL MEAL PREP *"},
    ]


st.title("Meal Maestro 🍲")
st.write("Welcome to Meal Maestro! Ask questions to customize your meal prep based on your preferences, dietary needs, and style!")


user_question = st.text_input("Enter your customizations:")

if user_question and (not st.session_state.get("last_question") or st.session_state.last_question != user_question):
  
    st.session_state.last_question = user_question
    
  
    chat = model.start_chat(
        history=[{"role": msg["role"], "parts": msg["text"]} for msg in st.session_state.history]
    )


    response = chat.send_message(user_question, stream=True)

    response_text = ""
    for chunk in response:
        response_text += chunk.text
    
  
    st.session_state.history.append({"role": "user", "text": user_question})
    st.session_state.history.append({"role": "model", "text": response_text})

# # Display the conversation history without duplication
message = st.session_state.history[-1] # trying for last one question
if message["role"] == "user":
    st.write(f"**You**: {message['text']}")
else:
        st.write(f"**Meal Maestro**: {message['text']}")

