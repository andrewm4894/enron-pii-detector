import streamlit as st
import pandas as pd
import random
import json
import os
from src.utils import clean_file_id, clean_message

# Set the page to wide mode
st.set_page_config(layout="wide")

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['file_id'] = df['file']
    return df

# Load the DataFrame from the specified path
df = load_data("./data/emails_train_small.csv")

# Function to list files in a folder
def list_files(folder_path):
    return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# Function to filter out already labeled files
def filter_labeled_files(files, labels_folder):
    labeled_files = set(list_files(labels_folder))
    return [f for f in files if f not in labeled_files]

# Function to extract file_id from filename
def extract_file_id(filename, path, tag):
    # read json file and extract file_id
    with open(f"{path}{filename}", "r") as f:
        data = json.load(f)
    return data["file_id"]

# Function to load a random row from the DataFrame based on file_id
def load_row_from_df(file_id, df):
    row = df[df['file_id'] == file_id].iloc[0]
    row["file_clean"] = clean_file_id(row["file"])
    row["message"] = clean_message(row["message"])
    return row

# Function to load a random row from the DataFrame
def load_random_row():
    row = df.sample(1).iloc[0]
    row["file_clean"] = clean_file_id(row["file"])
    row["message"] = clean_message(row["message"])
    return row

# Add a toggle to switch between sampling modes
sampling_mode = st.sidebar.radio("Select Sampling Mode", ("Default", "Folder Sampling"))

# Sidebar inputs for Folder Path and Tag
if sampling_mode == "Folder Sampling":
    folder_path = st.sidebar.text_input("Enter Folder Path", "./data/labels_llm/dev/")
    tag = st.sidebar.text_input("Enter Tag", "dev")

# Initialize session state for email data
if "email_data" not in st.session_state:
    st.session_state.email_data = load_random_row()

# Based on the sampling mode, load data
if sampling_mode == "Folder Sampling":
    labels_folder = "./data/labels/"
    if st.sidebar.button("Sample New File"):
        folder_files = list_files(folder_path)
        remaining_files = filter_labeled_files(folder_files, labels_folder)
        if not remaining_files:
            st.warning("No more files to label in the selected folder.")
        else:
            selected_file = random.choice(remaining_files)
            file_id = extract_file_id(selected_file, folder_path, tag)
            st.session_state.email_data = load_row_from_df(file_id, df)
else:
    if st.sidebar.button("Sample Another Email"):
        st.session_state.email_data = load_random_row()

# Layout
st.title("PII Data Labeler")

# Display the current email message
st.session_state.file_id = st.session_state.email_data["file_id"]
st.session_state.file_id_clean = st.session_state.email_data["file_clean"]
st.session_state.message = st.session_state.email_data["message"]

st.write("File ID:", st.session_state.file_id)
st.text_area("Email Message", st.session_state.message, height=500)

# Input boxes for PII in columns
st.subheader("Highlight and Enter PII Information")

col1, col2, col3, col4 = st.columns(4)
st.session_state.name = col1.text_area("Names", value="", height=100)
st.session_state.phone_number = col2.text_area("Phone Numbers", value="", height=100)
st.session_state.email_address = col3.text_area("Email Addresses", value="", height=100)
st.session_state.physical_address = col4.text_area("Physical Addresses", value="", height=100)

# Save Button
if st.button("Save PII Data"):
    pii_data = {
        "file_id": st.session_state.file_id,
        "names": list(set(st.session_state.name.split("\n"))),
        "phone_numbers": list(set(st.session_state.phone_number.split("\n"))),
        "email_addresses": list(set(st.session_state.email_address.split("\n"))),
        "physical_addresses": list(set(st.session_state.physical_address.split("\n"))),
    }
    for key in ["email_addresses"]:
        pii_data[key] = [x.lower() for x in pii_data[key]]

    output_path = f"./data/labels/{st.session_state.file_id_clean}.json"
    with open(output_path, "w") as f:
        json.dump(pii_data, f)

    st.success(f"PII data saved successfully! ({output_path})")
