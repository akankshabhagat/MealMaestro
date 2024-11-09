import requests
import streamlit as st

def image_url(prompt):
    width = 300
    height = 300
    seed = 5 # Each seed generates a new image variation
    model = 'turbo' # Using 'flux' as default if model is not provided

    image_url = f"https://pollinations.ai/p/{prompt}?width={width}&height={height}&seed={seed}&model={model}"
    return image_url

st.set_page_config(
    page_title="Image",
    page_icon="🖼️",
    layout="centered",
)

st.title("Ingredient Finder")
st.subheader("Search for Ingredients: ", divider="orange")
st.subheader("WARNING: This model is VERY VERY slow. Please be patient.")

input = st.text_input("Enter the prompt for the image")
if st.button("Generate Image"):
    with st.status("Generating Image..."):
        image = image_url(input)
        st.image(image, use_column_width=True)