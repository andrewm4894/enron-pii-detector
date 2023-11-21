import streamlit as st
import pandas as pd
import random
import json

# Set the page to wide mode
st.set_page_config(layout="wide")


@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)


# Load the DataFrame from the specified path
df = load_data("./data/emails_train_sample.csv")


# Function to load a random row from the DataFrame
def load_random_row():
    row = df.sample(1).iloc[0]
    row["file_clean"] = (
        row["file"].replace("/", "_").replace("-", "_").replace(".", "_")
    )
    row["message"] = "\n".join(row["message"].split("\n")[16:])
    return row


# Initialize session state for email data and PII inputs
if "email_data" not in st.session_state:
    st.session_state.email_data = load_random_row()
if "pii_inputs" not in st.session_state:
    st.session_state.pii_inputs = {
        "name": "",
        "phone_number": "",
        "email_address": "",
        "physical_address": "",
    }

# Layout
st.title("PII Data Labeler")

# Display the current email message
file_id = st.session_state.email_data["file"]
file_id_clean = st.session_state.email_data["file_clean"]
message = st.session_state.email_data["message"]

st.write("File ID:", file_id)
st.text_area("Email Message", message, height=500)

# Input boxes for PII in columns
st.subheader("Highlight and Enter PII Information")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.session_state.pii_inputs["name"] = st.text_area(
        "Names", st.session_state.pii_inputs["name"], height=100
    )
with col2:
    st.session_state.pii_inputs["phone_number"] = st.text_area(
        "Phone Numbers", st.session_state.pii_inputs["phone_number"], height=100
    )
with col3:
    st.session_state.pii_inputs["email_address"] = st.text_area(
        "Email Addresses", st.session_state.pii_inputs["email_address"], height=100
    )
with col4:
    st.session_state.pii_inputs["physical_address"] = st.text_area(
        "Physical Addresses",
        st.session_state.pii_inputs["physical_address"],
        height=100,
    )

# Save Button
if st.button("Save PII Data"):
    pii_data = {
        "file_id": file_id,
        "names": st.session_state.pii_inputs["name"].split("\n"),
        "phone_numbers": st.session_state.pii_inputs["phone_number"].split("\n"),
        "email_addresses": st.session_state.pii_inputs["email_address"].split("\n"),
        "physical_addresses": st.session_state.pii_inputs["physical_address"].split(
            "\n"
        ),
    }

    output_path = f"./data/labels/{file_id_clean}.json"
    with open(output_path, "w") as f:
        json.dump(pii_data, f)

    st.success(f"PII data saved successfully! ({output_path})")

# Button to load a new random email
if st.button("Sample Another Email"):
    st.session_state.email_data = load_random_row()
    file_id = st.session_state.email_data["file"]
    file_id_clean = st.session_state.email_data["file_clean"]
    message = st.session_state.email_data["message"]
    # Reset PII input fields
    st.session_state.pii_inputs = {
        "name": "",
        "phone_number": "",
        "email_address": "",
        "physical_address": "",
    }
