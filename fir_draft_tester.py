import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("FIR Drafting Endpoint Tester")

st.header("Draft a New FIR")

with st.form("fir_form"):
    complainant_name = st.text_input("Complainant Name", "Rahul Sharma")
    complainant_address = st.text_input("Complainant Address", "123 Main St, Mumbai")
    accused_name = st.text_input("Accused Name", "")
    incident_date = st.date_input("Incident Date")
    incident_time = st.time_input("Incident Time")
    incident_place = st.text_input("Incident Place", "Near City Park, Mumbai")
    incident_description = st.text_area("Incident Description", "The complainant was assaulted by an unknown person while walking in the park.")
    police_station = st.text_input("Police Station", "Mumbai Central")
    additional_details = st.text_area("Additional Details", "")
    submit = st.form_submit_button("Draft FIR")

if submit:
    payload = {
        "complainant_name": complainant_name,
        "complainant_address": complainant_address,
        "accused_name": accused_name,
        "incident_date": str(incident_date),
        "incident_time": str(incident_time),
        "incident_place": incident_place,
        "incident_description": incident_description,
        "police_station": police_station,
        "additional_details": additional_details
    }
    with st.spinner("Drafting FIR..."):
        try:
            response = requests.post(f"{API_URL}/fir/draft", json=payload)
            if response.status_code == 200:
                fir_text = response.json()["fir_text"]
                st.success("FIR Drafted Successfully!")
                st.code(fir_text, language="markdown")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")

st.header("Test /query Endpoint")
query = st.text_input("Ask a legal question", "What is the penalty for medical negligence under BNS?")
if st.button("Submit Query"):
    with st.spinner("Querying..."):
        try:
            resp = requests.post(f"{API_URL}/query", json={"question": query})
            if resp.status_code == 200:
                st.write("Response:")
                st.json(resp.json())
            else:
                st.error(f"Error: {resp.status_code} - {resp.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")