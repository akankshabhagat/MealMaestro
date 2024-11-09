import streamlit as st
from pymongo import MongoClient
import bcrypt

# MongoDB connection setup
client = MongoClient("mongodb+srv://rohannayakanti:2004%40Atlas@users.e7dcp.mongodb.net/")  # replace with your MongoDB connection string
db = client["auth_app"]  # Create a database called auth_app
users_collection = db["users"]  # Create a collection called users

# Helper function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Helper function to verify password
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password)

# Sign up function
def signup_user(username, password):
    if users_collection.find_one({"username": username}):
        return False  # Username already exists
    hashed_pw = hash_password(password)
    users_collection.insert_one({"username": username, "password": hashed_pw})
    return True

# Login function
def login_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and verify_password(user["password"], password):
        return True
    return False

# Streamlit UI
def main():
    st.title("MongoDB Atlas Streamlit Authentication App")

    if "Account" not in st.session_state:
        st.session_state['Account'] = []

    @st.dialog("Login/Sign up")
    def option(choice):

        if choice == "Login":
            st.subheader("Login Section", divider="orange")

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login", key="login"):
                if login_user(username, password):
                    st.success(f"Welcome {username}!")
                    st.write("You are logged in.")
                    st.session_state.Account = username
                else:
                    st.error("Invalid username or password")

        elif choice == "Signup":
            st.subheader("Create New Account")

            new_user = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            if st.button("Signup", key="Signup"):
                if signup_user(new_user, new_password):
                    st.success("Account created successfully!")
                    st.info("Go to the Login menu to log in.")
                else:
                    st.warning("Username already exists. Try a different one.")
    

    st.write("Login/Sign-up")
    if st.button("Login", key="choice1"):
        option("Login")
    if st.button("Signup", key="choice2"):
        option("Signup")


if __name__ == "__main__":
    main()
