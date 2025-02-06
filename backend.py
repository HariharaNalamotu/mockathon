import streamlit as st
print("streamlit")
import os
from PIL import Image
print("uvi")
import uvicorn
print("uvi")
import requests
from main import app
import threading


def save_image(image, path):
    image.save(path)


def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000)


def main():
    st.title("EcoScreen AI")

    uploaded_file = st.file_uploader("Upload an image")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Sunscreen Label")
        image_path = os.path.join(os.getcwd(), uploaded_file.name)

        if st.button("Save & Process Image"):
            save_image(Image.open(uploaded_file), image_path)

            url = f"http://127.0.0.1:8000/?path={image_path}"
            response = requests.post(url)
            response_dict = response.json()
            print(response_dict)
            response = response_dict['response']

            st.success(response)

if __name__ == "__main__":
    thread = threading.Thread(target=run_fastapi, daemon=True)
    thread.start()
    main()