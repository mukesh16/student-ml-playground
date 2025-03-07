import streamlit as st
import requests
import pandas as pd
import os

BASE_URL = "http://127.0.0.1:8000"

st.title("Student ML Playground 🚀")

# File Upload Section
st.header("Upload Your Dataset")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())

    response = requests.post(f"{BASE_URL}/upload/", files={"file": open(os.path.join('uploads', uploaded_file.name), "rb")})
    if response.status_code == 200:
        st.success(f"{uploaded_file.name} uploaded successfully!")
    else:
        st.error("Upload failed!")

# List Uploaded Files
st.header("Available Files")
files_response = requests.get(f"{BASE_URL}/files/")
if files_response.status_code == 200:
    files = files_response.json().get("files", [])
    if files:
        selected_file = st.selectbox("Select a file to preview", [f["filename"] for f in files])
        
        # Preview File
        if st.button("Preview Data"):
            preview_response = requests.get(f"{BASE_URL}/preview/?filename={selected_file}")
            if preview_response.status_code == 200:
                st.dataframe(pd.DataFrame(preview_response.json()))
            else:
                st.error("Error fetching preview data!")

        # Train Model
        st.header("Train a Model")
        target_column = st.text_input("Enter target column name:")
        if st.button("Train Model"):
            train_response = requests.post(f"{BASE_URL}/train/", params={"filename": selected_file, "target_column": target_column})
            if train_response.status_code == 200:
                result = train_response.json()
                st.success(f"Model trained successfully with accuracy: {result['accuracy']:.2f}")
            else:
                st.error("Model training failed!")
    else:
        st.warning("No files uploaded yet!")

# Run Backend First Message
st.sidebar.info("Make sure to start the backend with `uvicorn backend:app --reload` before using the UI.")
