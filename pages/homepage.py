import streamlit as st
import base64

# Convert local image to base64 for embedding
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Get base64 encoding of the local image
img_file = "backgroundmeal.jpg"
base64_img = get_base64_of_bin_file(img_file)

# Background CSS with main app and sidebar backgrounds
page_bg_img = f"""
<style>
 /* Main app background with gradient 
 [data-testid="stAppViewContainer"] {{
     background: linear-gradient(135deg, #CDE8E5, #EEF7FF, #7AB2B2, #4D869C);
     background-size: cover;
     background-position: center;
     background-repeat: no-repeat;
     background-attachment: fixed;
     color: black;
 }}
*/


/* Main app background 
[data-testid="stAppViewContainer"] {{
background-image: url("data:image/png;base64,{base64_img}");
background-size: 100%;
background-position: center;
background-position: cover;
background-repeat: no-repeat;
background-attachment: local;
color:black;
}}

*/

/* Sidebar background using local image in base64 */
[data-testid="stSidebar"] > div:first-child {{
    # background-image: url("data:image/png;base64,{base64_img}");
    background: linear-gradient(135deg, #CDE8E5, #EEF7FF, #7AB2B2, #4D869C);
    background-position: center; 
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{

      background: linear-gradient( #CDE8E5, #EEF7FF, #7AB2B2, #4D869C);
    background-size: cover;
    background-position: top right;
    background-repeat: no-repeat;
    background-attachment: fixed;
color: #333333;

}}

/* Transparent header and reposition toolbar */
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
    right: 2rem;
}}
</style>
"""

# Apply the custom CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

# Display the image and app content

st.sidebar.header("Configuration")

with st.container():
    st.title("Meal Maestro")
    st.header("Tagline")
    st.write("""
    MEAL Maestro is created by Aku, Rohan, and Krishna using Figma (UI/UX), MongoDB Atlas, Gemini API (for chatbot), 
    Streamlit, and Three.js for the globe visualization. It is a web app that provides a personalized meal plan 
    according to your dietary preferences.
    """)

    st.header("What Can You Use Meal Maestro For?")
    st.write("""
    Meal Maestro can help you find meal plans that suit your dietary needs, track your nutrition, and more!
    """)

    st.header("Try it Out!")
