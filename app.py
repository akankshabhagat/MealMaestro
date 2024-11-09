import streamlit as st

home = st.Page(
        "app.py",
        title = "Home",
        icon=":material/home:"
)

signup = st.Page(
        "pages/login_signup.py",
        title="Login/Signup"
)

if "Account" not in st.session_state:
        st.session_state['Account'] = []

st.title("Main Page")
# st.navigation({
#         "Your Account" : [Log_Out, Settings]
#     })

if st.button("Login/Signup"):
        st.switch_page("pages\login_signup.py")