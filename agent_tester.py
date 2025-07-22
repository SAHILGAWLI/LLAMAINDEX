import streamlit as st
import requests
import json
import time
from datetime import datetime

st.set_page_config(
    page_title="Legal Platform API Tester",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Legal Platform ReAct Agent API Tester")

# API Configuration
api_url = st.text_input("API Base URL", value="http://localhost:8000")

# Sidebar for navigation
st.sidebar.title("🧪 Test Sections")
test_section = st.sidebar.radio(
    "Choose Test Type",
    [
        "🏠 Dashboard Population",
        "📋 Individual Grids", 
        "🔄 Real-time Streaming",
        "💬 Original Chat APIs",
        "🏥 Health & Status"
    ]
)

# Helper function to make API calls
def make_api_call(endpoint, method="GET", data=None):
    try:
        url = f"{api_url}{endpoint}"
        
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

# Helper function to display JSON nicely
def display_json(data, title="Response"):
    st.subheader(title)
    st.json(data)

# ---------------------------------------------
# Dashboard Population Testing
# ---------------------------------------------
if test_section == "🏠 Dashboard Population":
    st.header("Dashboard Population Testing")
    st.write("Test the master endpoint that populates all 4 grids using ReAct agents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        case_id = st.text_input("Case ID", value="CASE-2024-001", key="dash_case_id")
        case_context = st.text_area(
            "Case Context", 
            value="Medical malpractice case involving surgical complications at City Hospital",
            key="dash_context"
        )
        user_role = st.selectbox("User Role", ["analyst", "lawyer", "compliance_officer"], key="dash_role")
        jurisdiction = st.text_input("Jurisdiction", value="Maharashtra", key="dash_jurisdiction")
    
    with col2:
        st.subheader("Request Preview")
        request_data = {
            "case_id": case_id,
            "case_context": case_context,
            "user_role": user_role,
            "jurisdiction": jurisdiction
        }
        st.json(request_data)
    
    if st.button("🚀 Populate Dashboard", type="primary"):
        with st.spinner("Running ReAct agents... This may take 30-60 seconds"):
            start_time = time.time()
            
            response_data, status_code = make_api_call(
                "/dashboard/populate", 
                method="POST", 
                data=request_data
            )
            
            end_time = time.time()
            
            if status_code == 200:
                st.success(f"✅ Dashboard populated successfully in {end_time - start_time:.2f} seconds!")
                
                # Display each grid's data
                tabs = st.tabs(["📋 Compliance", "⚖️ Laws", "📄 Documents", "📁 Cases", "📊 Summary"])
                
                with tabs[0]:
                    if "grid_1_compliance" in response_data:
                        compliance_data = response_data["grid_1_compliance"]
                        st.subheader("FHIR Compliance Checklist")
                        
                        # Progress bar
                        progress = compliance_data.get("percentage", 0)
                        st.progress(progress / 100)
                        st.write(f"Progress: {compliance_data.get('progress', 'N/A')} ({progress}%)")
                        
                        # Checklist items
                        for item in compliance_data.get("checklist_items", []):
                            status_emoji = "✅" if item["status"] == "completed" else "⏳" if item["status"] == "pending" else "❌"
                            st.write(f"{status_emoji} {item['item']}")
                
                with tabs[1]:
                    if "grid_2_laws" in response_data:
                        laws_data = response_data["grid_2_laws"]
                        st.subheader("Relevant BNS Laws")
                        
                        for law in laws_data.get("laws", []):
                            severity_color = "🔴" if law["severity"] == "High" else "🟡" if law["severity"] == "Medium" else "🟢"
                            st.write(f"{severity_color} **Section {law['section']}**: {law['title']}")
                            st.write(f"   Relevance: {law['relevance_score']:.2f}")
                            if law.get("description"):
                                st.write(f"   {law['description']}")
                            st.write("---")
                
                with tabs[2]:
                    if "grid_3_documents" in response_data:
                        docs_data = response_data["grid_3_documents"]
                        st.subheader("Case Documents")
                        
                        for doc in docs_data.get("documents", []):
                            priority_emoji = "🔥" if doc["priority"] == "high" else "📋" if doc["priority"] == "medium" else "📄"
                            st.write(f"{priority_emoji} **{doc['name']}**")
                            st.write(f"   Type: {doc['type']}")
                            st.write(f"   Summary: {doc['summary']}")
                            st.write("---")
                
                with tabs[3]:
                    if "grid_4_cases" in response_data:
                        cases_data = response_data["grid_4_cases"]
                        st.subheader("Similar Past Cases")
                        
                        for case in cases_data.get("cases", []):
                            similarity_bar = "🟩" * int(case["similarity_score"] * 10) + "⬜" * (10 - int(case["similarity_score"] * 10))
                            st.write(f"**{case['title']}** ({case['case_id']})")
                            st.write(f"   Similarity: {similarity_bar} {case['similarity_score']:.2f}")
                            st.write(f"   Status: {case['status']} | Outcome: {case.get('outcome', 'N/A')}")
                            st.write("---")
                
                with tabs[4]:
                    st.subheader("Generation Summary")
                    st.metric("Generation Time", f"{response_data.get('generation_time', 0):.2f}s")
                    st.metric("AI Confidence", f"{response_data.get('ai_confidence', 0):.2f}")
                    
                    # Raw response
                    with st.expander("Raw Response Data"):
                        st.json(response_data)
            else:
                st.error(f"❌ Error {status_code}: {response_data}")

# ---------------------------------------------
# Individual Grid Testing
# ---------------------------------------------
elif test_section == "📋 Individual Grids":
    st.header("Individual Grid Testing")
    st.write("Test each grid endpoint separately")
    
    grid_type = st.selectbox(
        "Select Grid",
        ["compliance", "laws", "documents", "cases"],
        format_func=lambda x: {
            "compliance": "📋 Grid 1: FHIR Compliance",
            "laws": "⚖️ Grid 2: BNS Laws",
            "documents": "📄 Grid 3: Documents",
            "cases": "📁 Grid 4: Past Cases"
        }[x]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        case_id = st.text_input("Case ID", value="CASE-2024-001", key="grid_case_id")
        context = st.text_area("Context", value="Medical malpractice case", key="grid_context")
    
    with col2:
        request_data = {
            "case_id": case_id,
            "context": context
        }
        st.subheader("Request Data")
        st.json(request_data)
    
    if st.button(f"🔍 Test {grid_type.title()} Grid"):
        with st.spinner(f"Running {grid_type} agent..."):
            response_data, status_code = make_api_call(
                f"/grid/{grid_type}",
                method="POST",
                data=request_data
            )
            
            if status_code == 200:
                st.success(f"✅ {grid_type.title()} grid loaded successfully!")
                display_json(response_data, f"{grid_type.title()} Grid Response")
            else:
                st.error(f"❌ Error {status_code}: {response_data}")

# ---------------------------------------------
# Real-time Streaming Testing
# ---------------------------------------------
elif test_section == "🔄 Real-time Streaming":
    st.header("Real-time Streaming Testing")
    st.write("Test WebSocket streaming for real-time dashboard updates")
    
    st.warning("⚠️ WebSocket testing requires a WebSocket client. Use the browser console or a WebSocket testing tool.")
    
    st.subheader("WebSocket Connection Details")
    ws_url = f"ws://localhost:8000/dashboard/stream"
    st.code(ws_url)
    
    st.subheader("Sample WebSocket Message")
    sample_message = {
        "case_id": "CASE-2024-001",
        "case_context": "Medical malpractice case involving surgical complications"
    }
    st.json(sample_message)
    
    st.subheader("JavaScript WebSocket Test Code")
    js_code = f"""
const ws = new WebSocket('{ws_url}');

ws.onopen = function(event) {{
    console.log('Connected to WebSocket');
    
    // Send test message
    ws.send(JSON.stringify({json.dumps(sample_message)}));
}};

ws.onmessage = function(event) {{
    const data = JSON.parse(event.data);
    console.log('Received:', data);
}};

ws.onclose = function(event) {{
    console.log('WebSocket closed');
}};
"""
    st.code(js_code, language="javascript")

# ---------------------------------------------
# Original Chat APIs Testing
# ---------------------------------------------
elif test_section == "💬 Original Chat APIs":
    st.header("Original Chat APIs Testing")
    st.write("Test the existing chat endpoints")
    
    # Single Query Test
    st.subheader("Single Query Test")
    query_question = st.text_input("Enter your question:", key="single_query")
    
    if st.button("Ask Single Query"):
        if query_question:
            response_data, status_code = make_api_call(
                "/query",
                method="POST",
                data={"question": query_question}
            )
            
            if status_code == 200:
                st.success("✅ Query successful!")
                st.write("**Answer:**", response_data.get("answer", "No answer"))
            else:
                st.error(f"❌ Error: {response_data}")
    
    # Multi-turn Chat Test
    st.subheader("Multi-turn Chat Test")
    
    if "chat_session_id" not in st.session_state:
        st.session_state.chat_session_id = f"session_{int(time.time())}"
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    st.write(f"Session ID: `{st.session_state.chat_session_id}`")
    
    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.write(f"**You:** {msg['text']}")
        else:
            st.write(f"**Bot:** {msg['text']}")
    
    chat_message = st.text_input("Chat message:", key="chat_input")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Send Chat Message"):
            if chat_message:
                # Add user message to history
                st.session_state.chat_history.append({"role": "user", "text": chat_message})
                
                # Send to API
                response_data, status_code = make_api_call(
                    "/chat",
                    method="POST",
                    data={
                        "session_id": st.session_state.chat_session_id,
                        "message": chat_message
                    }
                )
                
                if status_code == 200:
                    answer = response_data.get("answer", "No answer")
                    st.session_state.chat_history.append({"role": "bot", "text": answer})
                    st.rerun()
                else:
                    st.error(f"Error: {response_data}")
    
    with col2:
        if st.button("Reset Chat"):
            st.session_state.chat_session_id = f"session_{int(time.time())}"
            st.session_state.chat_history = []
            st.rerun()

# ---------------------------------------------
# Health & Status Testing
# ---------------------------------------------
elif test_section == "🏥 Health & Status":
    st.header("Health & Status Testing")
    st.write("Check API health and agent status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Health Check")
        if st.button("🏥 Check Health"):
            response_data, status_code = make_api_call("/health")
            
            if status_code == 200:
                st.success("✅ API is healthy!")
                st.metric("Status", response_data.get("status", "unknown"))
                st.metric("Version", response_data.get("version", "unknown"))
                st.write("**Available Agents:**", response_data.get("agents_available", []))
            else:
                st.error(f"❌ Health check failed: {response_data}")
    
    with col2:
        st.subheader("Agent Status")
        if st.button("🤖 Check Agents"):
            response_data, status_code = make_api_call("/agents/status")
            
            if status_code == 200:
                st.success("✅ Agent status retrieved!")
                st.metric("Total Agents", response_data.get("total_agents", 0))
                
                agents = response_data.get("agents", {})
                for name, info in agents.items():
                    st.write(f"**{name}**: {info.get('status', 'unknown')} ({info.get('tools_count', 0)} tools)")
            else:
                st.error(f"❌ Agent status failed: {response_data}")
    
    # Root endpoint info
    st.subheader("API Information")
    if st.button("ℹ️ Get API Info"):
        response_data, status_code = make_api_call("/")
        
        if status_code == 200:
            st.success("✅ API info retrieved!")
            display_json(response_data, "API Information")
        else:
            st.error(f"❌ Failed to get API info: {response_data}")

# Footer
st.markdown("---")
st.markdown("**Legal Platform ReAct Agent API Tester** | Built with Streamlit")
st.markdown("Test all aspects of the intelligent legal platform API with ReAct agents")
