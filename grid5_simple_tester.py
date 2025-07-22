#!/usr/bin/env python3
"""
Simple Grid 5 Live Cases Tester
Works with minimal_server.py for immediate testing
"""

import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Grid 5: Live Cases Analytics Tester",
    page_icon="🏛️",
    layout="wide"
)

# Title and description
st.title("🏛️ Grid 5: Live Cases Analytics Tester")
st.markdown("**Test the new Grid 5 Live Cases Analytics API with real-time legal case data**")

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Sidebar for configuration
st.sidebar.header("🔧 Configuration")
st.sidebar.markdown("**API Server:** `localhost:8000`")
st.sidebar.markdown("**Status:** 🟢 Demo Mode Active")

# Check server status
try:
    response = requests.get(f"{API_BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        st.sidebar.success("✅ Server is running")
        health_data = response.json()
        st.sidebar.json(health_data)
    else:
        st.sidebar.error("❌ Server error")
except Exception as e:
    st.sidebar.error(f"❌ Cannot connect to server: {e}")

# Main content area
st.header("🔍 Test Grid 5 Live Cases")

# Input form
with st.form("grid5_test_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        case_id = st.text_input("Case ID", value="CASE-2024-001", help="Unique identifier for the case")
        case_context = st.text_area(
            "Case Context", 
            value="Medical negligence case involving surgical complications during routine procedure",
            height=100,
            help="Describe the legal case context"
        )
    
    with col2:
        additional_context = st.text_area(
            "Additional Context (Optional)",
            value="Patient suffered complications during routine surgery. Hospital failed to follow standard protocols.",
            height=100,
            help="Any additional context or details"
        )
    
    submitted = st.form_submit_button("🚀 Analyze Live Cases", type="primary")

if submitted:
    st.header("📊 Grid 5 Analysis Results")
    
    # Prepare request data
    request_data = {
        "case_id": case_id,
        "case_context": case_context,
        "additional_context": additional_context
    }
    
    # Show request being sent
    with st.expander("📤 Request Data", expanded=False):
        st.json(request_data)
    
    # Make API call
    try:
        with st.spinner("🔄 Analyzing live cases..."):
            response = requests.post(
                f"{API_BASE_URL}/grid/live-cases",
                json=request_data,
                timeout=30
            )
        
        if response.status_code == 200:
            result = response.json()
            
            # Display success message
            st.success(f"✅ {result['message']}")
            
            # Display metadata
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Cases Found", result['total_cases'])
            with col2:
                st.metric("Generation Time", f"{result['generation_time']:.2f}s")
            with col3:
                st.metric("Status", result['status'].upper())
            
            # Display cases
            st.subheader("⚖️ Relevant Legal Cases")
            
            for i, case in enumerate(result['cases'], 1):
                with st.expander(f"📋 Case {i}: {case['title']}", expanded=True):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Court:** {case['court']}")
                        st.markdown(f"**Date:** {case['date']}")
                        st.markdown(f"**Citation:** {case['citation']}")
                        st.markdown(f"**Summary:** {case['summary']}")
                        if case['url']:
                            st.markdown(f"**URL:** [View Case]({case['url']})")
                    
                    with col2:
                        # Similarity score with color coding
                        score = case['similarity_score']
                        if score >= 0.9:
                            st.success(f"🎯 Similarity: {score:.1%}")
                        elif score >= 0.8:
                            st.warning(f"🔶 Similarity: {score:.1%}")
                        else:
                            st.info(f"🔵 Similarity: {score:.1%}")
                        
                        # Court hierarchy indicator
                        if "Supreme Court" in case['court']:
                            st.markdown("🏛️ **Supreme Court**")
                        elif "High Court" in case['court']:
                            st.markdown("🏢 **High Court**")
                        else:
                            st.markdown("🏛️ **District Court**")
            
            # Raw response
            with st.expander("📥 Raw API Response", expanded=False):
                st.json(result)
                
        else:
            st.error(f"❌ API Error: {response.status_code}")
            st.code(response.text)
            
    except Exception as e:
        st.error(f"❌ Error: {e}")

# Test other endpoints
st.header("🧪 Additional Tests")

col1, col2 = st.columns(2)

with col1:
    if st.button("🏠 Test Root Endpoint"):
        try:
            response = requests.get(f"{API_BASE_URL}/")
            if response.status_code == 200:
                st.success("✅ Root endpoint working")
                st.json(response.json())
            else:
                st.error(f"❌ Error: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Error: {e}")

with col2:
    if st.button("📊 Test System Status"):
        try:
            response = requests.get(f"{API_BASE_URL}/system/status")
            if response.status_code == 200:
                st.success("✅ System status retrieved")
                st.json(response.json())
            else:
                st.error(f"❌ Error: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# Demo cases
st.header("🎭 Demo Cases")
if st.button("📋 View All Demo Cases"):
    try:
        response = requests.get(f"{API_BASE_URL}/demo/cases")
        if response.status_code == 200:
            demo_data = response.json()
            st.success(f"✅ {demo_data['message']}")
            
            for i, case in enumerate(demo_data['cases'], 1):
                with st.expander(f"Demo Case {i}: {case['title']}"):
                    st.markdown(f"**Court:** {case['court']}")
                    st.markdown(f"**Date:** {case['date']}")
                    st.markdown(f"**Citation:** {case['citation']}")
                    st.markdown(f"**Summary:** {case['summary']}")
                    st.markdown(f"**Similarity Score:** {case['similarity_score']:.1%}")
        else:
            st.error(f"❌ Error: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# Footer
st.markdown("---")
st.markdown("**🏛️ Grid 5: Live Cases Analytics** | Demo Mode | Legal Platform v2.0.0")
st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
