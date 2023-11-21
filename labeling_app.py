import streamlit as st
import pandas as pd
import random
import json
from src.utils import clean_file_id, clean_message

# Set the page to wide mode
st.set_page_config(layout="wide")

@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Load the DataFrame from the specified path
df = load_data("./data/emails_train_small.csv")

# Function to load a random row from the DataFrame
def load_random_row():
    row = df.sample(1).iloc[0]
    row["file_clean"] = clean_file_id(row["file"])
    row["message"] = clean_message(row["message"])
    return row

# Initialize session state for email data
if "email_data" not in st.session_state:
    st.session_state.email_data = load_random_row()

# Layout
st.title("PII Data Labeler")

# Display the current email message
st.session_state.file_id = st.session_state.email_data["file"]
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

# Button to load a new random email
if st.button("Sample Another Email"):
    st.session_state.email_data = load_random_row()
    st.rerun()
