import streamlit as st
import requests
import json

API_URL = "http://localhost:8000"

st.title("FIR Intelligence Dashboard Tester")

st.header("FIR Fields Input")
with st.form("fir_form"):
    complainant_name = st.text_input("Complainant Name", "Rahul Sharma")
    complainant_address = st.text_input("Complainant Address", "123 Main St, Mumbai")
    accused_name = st.text_input("Accused Name", "")
    incident_date = st.date_input("Incident Date")
    incident_time = st.time_input("Incident Time")
    incident_place = st.text_input("Incident Place", "Near City Park, Mumbai")
    incident_description = st.text_area("Incident Description", "The complainant suffered injury due to negligence by the accused.")
    police_station = st.text_input("Police Station", "Mumbai Central")
    additional_details = st.text_area("Additional Details", "No witnesses were present.")
    submit = st.form_submit_button("Analyze FIR")

if submit:
    fir_fields = {
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
    with st.spinner("Analyzing FIR..."):
        try:
            response = requests.post(f"{API_URL}/fir/intelligence-dashboard", json={"fir_fields": fir_fields})
            if response.status_code == 200:
                data = response.json()
                st.success("FIR Intelligence Analysis Complete!")
                st.subheader("FIR Draft")
                st.code(data["fir_text"], language="markdown")
                st.subheader("Grid 1: Suggested Sections")
                st.write(data["grid_1_sections"])
                st.subheader("Grid 2: Completeness Checklist")
                st.write(data["grid_2_completeness"])
                st.subheader("Grid 3: Best Practices Tips")
                st.write(data["grid_3_best_practices"])
                st.info(f"Generation Time: {data['generation_time']}s | AI Confidence: {data['ai_confidence']}")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")
