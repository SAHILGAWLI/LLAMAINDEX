import streamlit as st
import requests
import uuid
import os
import json
import time
from typing import Dict, Any

# Page configuration
st.set_page_config(
    page_title="Legal Platform ReAct Agent API Tester",
    page_icon="🏛️",
    layout="wide"
)

st.title("🏛️ Legal Platform ReAct Agent API Tester")
st.markdown("---")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Environment Variables Setup
    st.subheader("🔑 Environment Variables")
    openai_key = st.text_input("OpenAI API Key", type="password", help="Your OpenAI API key")
    pinecone_key = st.text_input("Pinecone API Key", type="password", help="Your Pinecone API key")
    pinecone_index = st.text_input("Pinecone Index Name", value="quickstart", help="Pinecone index name")
    
    # Grid 5 Configuration
    st.subheader("🏛️ Grid 5: Indian Kanoon API")
    indian_kanoon_key = st.text_input("Indian Kanoon API Token", type="password", help="Your Indian Kanoon API token for live legal case data")
    st.markdown("*Required for Grid 5 Live Cases Analytics*")
    
    if st.button("💾 Set Environment Variables"):
        if openai_key and pinecone_key:
            os.environ["OPENAI_API_KEY"] = openai_key
            os.environ["PINECONE_API_KEY"] = pinecone_key
            os.environ["PINECONE_INDEX_NAME"] = pinecone_index
            os.environ["LLM_MODEL"] = "gpt-4o-mini"
            os.environ["EMBEDDING_MODEL"] = "text-embedding-3-small"
            
            # Set Indian Kanoon API token if provided
            if indian_kanoon_key:
                os.environ["INDIAN_KANOON_API_TOKEN"] = indian_kanoon_key
                st.success("✅ All environment variables set! Grid 5 Live Mode enabled!")
            else:
                st.success("✅ Basic environment variables set! Add Indian Kanoon token for Grid 5 Live Mode.")
        else:
            st.error("❌ Please provide both OpenAI and Pinecone API keys")
    
    st.markdown("---")
    
    # API Configuration
    st.subheader("🌐 API Configuration")
    api_url = st.text_input("API Base URL", value="http://localhost:8000")
    
    # Connection Test
    if st.button("🔍 Test Connection"):
        try:
            response = requests.get(f"{api_url}/", timeout=5)
            if response.status_code == 200:
                st.success("✅ API is reachable!")
                st.json(response.json())
            else:
                st.error(f"❌ API returned status {response.status_code}")
        except Exception as e:
            st.error(f"❌ Connection failed: {e}")
    
    # Health Check
    if st.button("🏥 Health Check"):
        try:
            response = requests.get(f"{api_url}/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                st.success("✅ System is healthy!")
                st.json(health_data)
            else:
                st.error(f"❌ Health check failed: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Health check error: {e}")

# Main content area with tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🤖 ReAct Agents", 
    "📊 Dashboard", 
    "💬 Chat APIs", 
    "🔍 Query API", 
    "📡 Streaming", 
    "📈 Status",
    "🏛️ Grid 5: Live Cases"
])

# Tab 1: ReAct Agents Testing
with tab1:
    st.header("🤖 Individual ReAct Agent Testing")
    
    col1, col2 = st.columns(2)
    
    # Shared inputs for individual grid testing
    st.subheader("📝 Test Parameters")
    col_params1, col_params2 = st.columns(2)
    with col_params1:
        test_case_id = st.text_input("Case ID for Testing:", value="TEST-2024-001", key="test_case_id")
    with col_params2:
        test_context = st.text_input("Case Context:", value="Medical malpractice case involving surgical negligence", key="test_context")
    
    st.markdown("---")
    
    with col1:
        st.subheader("⚖️ Compliance Agent")
        st.info("Generates FHIR compliance checklists for medical cases")
        if st.button("🔍 Test Compliance Agent"):
            try:
                start_time = time.time()
                response = requests.post(f"{api_url}/grid/compliance", 
                    json={
                        "case_id": test_case_id,
                        "context": test_context
                    })
                end_time = time.time()
                
                if response.status_code == 200:
                    st.success(f"✅ Response received in {end_time - start_time:.2f}s")
                    st.json(response.json())
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"❌ Request failed: {e}")
        
        st.subheader("📚 Legal Laws Agent")
        st.info("Finds relevant BNS law sections with severity classification")
        if st.button("🔍 Test Laws Agent"):
            try:
                start_time = time.time()
                response = requests.post(f"{api_url}/grid/laws", 
                    json={
                        "case_id": test_case_id,
                        "context": test_context
                    })
                end_time = time.time()
                
                if response.status_code == 200:
                    st.success(f"✅ Response received in {end_time - start_time:.2f}s")
                    st.json(response.json())
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"❌ Request failed: {e}")
    
    with col2:
        st.subheader("📄 Document Agent")
        st.info("Analyzes and prioritizes documents by type and relevance")
        if st.button("🔍 Test Document Agent"):
            try:
                start_time = time.time()
                response = requests.post(f"{api_url}/grid/documents", 
                    json={
                        "case_id": test_case_id,
                        "context": test_context
                    })
                end_time = time.time()
                
                if response.status_code == 200:
                    st.success(f"✅ Response received in {end_time - start_time:.2f}s")
                    st.json(response.json())
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"❌ Request failed: {e}")
        
        st.subheader("🏛️ Case Analysis Agent")
        st.info("Finds similar past cases with similarity scores")
        if st.button("🔍 Test Case Agent"):
            try:
                start_time = time.time()
                response = requests.post(f"{api_url}/grid/cases", 
                    json={
                        "case_id": test_case_id,
                        "context": test_context
                    })
                end_time = time.time()
                
                if response.status_code == 200:
                    st.success(f"✅ Response received in {end_time - start_time:.2f}s")
                    st.json(response.json())
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"❌ Request failed: {e}")

# Tab 2: Dashboard Population Testing
with tab2:
    st.header("📊 Dashboard Population Testing")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        case_id = st.text_input("Case ID:", value="CASE-2024-001", key="dash_case_id")
        case_context = st.text_area("Case Context:", 
            value="Medical malpractice case involving surgical negligence and patient harm. Requires FHIR compliance review and BNS law analysis.",
            height=100, key="dash_context")
    
    with col2:
        st.info("📋 Choose execution strategy for dashboard population")
        
        execution_mode = st.radio(
            "Execution Strategy:",
            ["🔄 Parallel (4 Grids - Fast)", "🎯 Hierarchical (5 Grids - Optimal)"],
            help="Choose between parallel execution (4 grids, faster) or hierarchical execution (5 grids with Grid 5 Live Cases, better results)"
        )
        
        if execution_mode == "🔄 Parallel (4 Grids - Fast)":
            endpoint = "/dashboard/populate"
            button_text = "🔄 Populate Dashboard (4 Grids - Parallel)"
            description = "Running 4 agents simultaneously..."
        else:
            endpoint = "/dashboard/populate-hierarchical"
            button_text = "🎯 Populate Dashboard (5 Grids - Hierarchical)"
            description = "Running 5 agents in optimal dependency order with Grid 5 Live Cases..."
        
        if st.button(button_text, type="primary"):
            try:
                with st.spinner(f"🔄 {description}"):
                    start_time = time.time()
                    response = requests.post(f"{api_url}{endpoint}", 
                        json={
                            "case_id": case_id,
                            "case_context": case_context
                        })  # No timeout - let it run as long as needed
                    end_time = time.time()
                
                if response.status_code == 200:
                    dashboard_data = response.json()
                    st.success(f"✅ Dashboard populated in {end_time - start_time:.2f}s")
                    
                    # Display results in organized format
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("⚖️ Grid 1: Compliance")
                        st.json(dashboard_data.get("grid_1_compliance", {}))
                        
                        st.subheader("📚 Grid 2: Laws")
                        st.json(dashboard_data.get("grid_2_laws", {}))
                    
                    with col2:
                        st.subheader("📄 Grid 3: Documents")
                        st.json(dashboard_data.get("grid_3_documents", {}))
                        
                        st.subheader("🏛️ Grid 4: Cases")
                        st.json(dashboard_data.get("grid_4_cases", {}))
                    
                    # Grid 5: Live Cases (if available)
                    if dashboard_data.get("grid_5_live_cases"):
                        st.subheader("🔍 Grid 5: Live Cases Analytics")
                        grid5_data = dashboard_data["grid_5_live_cases"]
                        
                        # Display Grid 5 metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Cases", grid5_data.get('total_cases', 0))
                        with col2:
                            st.metric("API Mode", grid5_data.get('api_mode', 'demo').upper())
                        with col3:
                            st.metric("Status", grid5_data.get('status', 'unknown').upper())
                        
                        # Display message
                        if grid5_data.get('message'):
                            if 'LIVE' in grid5_data['message']:
                                st.success(f"✅ {grid5_data['message']}")
                            elif 'DEMO' in grid5_data['message']:
                                st.warning(f"⚠️ {grid5_data['message']}")
                            else:
                                st.info(f"ℹ️ {grid5_data['message']}")
                        
                        # Display cases
                        if grid5_data.get('cases'):
                            st.write("**Top Relevant Cases:**")
                            for i, case in enumerate(grid5_data['cases'][:3], 1):  # Show top 3
                                with st.expander(f"Case {i}: {case.get('title', 'Unknown')}", expanded=False):
                                    st.write(f"**Court:** {case.get('court', 'Unknown')}")
                                    st.write(f"**Date:** {case.get('date', 'Unknown')}")
                                    st.write(f"**Similarity:** {case.get('similarity_score', 0):.1%}")
                                    st.write(f"**Summary:** {case.get('summary', 'No summary available')}")
                        
                        # Raw Grid 5 data
                        with st.expander("📥 Raw Grid 5 Data", expanded=False):
                            st.json(grid5_data)
                    
                    # Metadata
                    st.subheader("📈 Metadata")
                    metadata = {
                        "Generation Time": f"{dashboard_data.get('generation_time', 0):.2f}s",
                        "AI Confidence": f"{dashboard_data.get('ai_confidence', 0):.2%}",
                        "Grids Populated": "5 (with Live Cases)" if dashboard_data.get("grid_5_live_cases") else "4 (standard)",
                        "Timestamp": dashboard_data.get('timestamp', 'N/A')
                    }
                    st.json(metadata)
                    
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"❌ Request failed: {e}")

# Tab 3: Chat APIs Testing
with tab3:
    st.header("💬 Chat APIs Testing")
    
    # Initialize session states
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid.uuid4())
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "citizen_session_id" not in st.session_state:
        st.session_state["citizen_session_id"] = str(uuid.uuid4())
    if "citizen_chat_history" not in st.session_state:
        st.session_state["citizen_chat_history"] = []
    
    def add_to_history(role, text):
        st.session_state["chat_history"].append({"role": role, "text": text})
    
    def add_to_citizen_history(role, text):
        st.session_state["citizen_chat_history"].append({"role": role, "text": text})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💬 Multi-turn Chat (condense_plus_context)")
        
        # Display chat history
        for msg in st.session_state["chat_history"]:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['text']}")
            else:
                st.markdown(f"**Bot:** {msg['text']}")
        
        chat_question = st.text_input("Your message:", key="multi_chat")
        
        col_send, col_reset = st.columns(2)
        with col_send:
            if st.button("📤 Send", key="send_chat"):
                if chat_question.strip():
                    add_to_history("user", chat_question)
                    try:
                        resp = requests.post(f"{api_url}/chat", json={
                            "session_id": st.session_state["session_id"],
                            "message": chat_question
                        })
                        answer = resp.json().get("answer", resp.text)
                        add_to_history("bot", answer)
                    except Exception as e:
                        st.error(f"Error: {e}")
                    st.rerun()
        
        with col_reset:
            if st.button("🔄 Reset", key="reset_chat"):
                st.session_state["session_id"] = str(uuid.uuid4())
                st.session_state["chat_history"] = []
                st.success("Chat session reset!")
                st.rerun()
    
    with col2:
        st.subheader("👤 Citizen Chat (condense_question)")
        
        # Display citizen chat history
        for msg in st.session_state["citizen_chat_history"]:
            if msg["role"] == "user":
                st.markdown(f"**You (Citizen):** {msg['text']}")
            else:
                st.markdown(f"**Bot:** {msg['text']}")
        
        citizen_chat_question = st.text_input("Your message:", key="citizen_chat")
        
        col_send, col_reset = st.columns(2)
        with col_send:
            if st.button("📤 Send", key="send_citizen"):
                if citizen_chat_question.strip():
                    add_to_citizen_history("user", citizen_chat_question)
                    try:
                        resp = requests.post(f"{api_url}/citizen_chat", json={
                            "session_id": st.session_state["citizen_session_id"],
                            "message": citizen_chat_question
                        })
                        answer = resp.json().get("answer", resp.text)
                        add_to_citizen_history("bot", answer)
                    except Exception as e:
                        st.error(f"Error: {e}")
                    st.rerun()
        
        with col_reset:
            if st.button("🔄 Reset", key="reset_citizen"):
                st.session_state["citizen_session_id"] = str(uuid.uuid4())
                st.session_state["citizen_chat_history"] = []
                st.success("Citizen chat session reset!")
                st.rerun()

# Tab 4: Query API Testing
with tab4:
    st.header("🔍 Single-turn Query Testing")
    
    query_question = st.text_area("Enter your question:", 
        value="What are the key provisions of BNS Section 103 regarding murder?",
        height=100, key="single_query")
    
    if st.button("🔍 Ask Question", type="primary"):
        try:
            start_time = time.time()
            resp = requests.post(f"{api_url}/query", json={"question": query_question})
            end_time = time.time()
            
            if resp.status_code == 200:
                st.success(f"✅ Response received in {end_time - start_time:.2f}s")
                answer = resp.json().get("answer", resp.text)
                st.markdown(f"**Answer:** {answer}")
            else:
                st.error(f"❌ Error {resp.status_code}: {resp.text}")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# Tab 5: Streaming Testing
with tab5:
    st.header("📡 Streaming API Testing")
    
    st.info("🚧 WebSocket streaming testing - Implementation in progress")
    
    streaming_message = st.text_input("Message for streaming:", 
        value="Explain the legal implications of cybercrime under BNS",
        key="streaming_msg")
    
    if st.button("🌊 Test Streaming"):
        try:
            # Test citizen chat streaming endpoint
            resp = requests.post(f"{api_url}/citizen_chat_stream", json={
                "session_id": str(uuid.uuid4()),
                "message": streaming_message
            }, stream=True)
            
            if resp.status_code == 200:
                st.success("✅ Streaming response:")
                response_container = st.empty()
                full_response = ""
                
                for line in resp.iter_lines():
                    if line:
                        full_response += line.decode('utf-8')
                        response_container.markdown(full_response)
            else:
                st.error(f"❌ Streaming failed: {resp.status_code}")
        except Exception as e:
            st.error(f"❌ Streaming error: {e}")

# Tab 6: Status and Monitoring
with tab6:
    st.header("📈 System Status & Monitoring")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Refresh Agent Status"):
            try:
                response = requests.get(f"{api_url}/agents/status")
                if response.status_code == 200:
                    st.success("✅ Agent Status:")
                    st.json(response.json())
                else:
                    st.error(f"❌ Status check failed: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Status error: {e}")
    
    with col2:
        if st.button("🏥 System Health Check"):
            try:
                response = requests.get(f"{api_url}/health")
                if response.status_code == 200:
                    health_data = response.json()
                    st.success("✅ System Health:")
                    st.json(health_data)
                else:
                    st.error(f"❌ Health check failed: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Health check error: {e}")
    
    # Environment status
    st.subheader("🌍 Environment Status")
    env_status = {
        "OpenAI API Key": "✅ Set" if os.getenv("OPENAI_API_KEY") else "❌ Missing",
        "Pinecone API Key": "✅ Set" if os.getenv("PINECONE_API_KEY") else "❌ Missing",
        "Pinecone Index": os.getenv("PINECONE_INDEX_NAME", "Not set"),
        "Indian Kanoon API Token": "✅ Set - Grid 5 Live Mode" if os.getenv("INDIAN_KANOON_API_TOKEN") else "❌ Missing - Demo Mode Only",
        "LLM Model": os.getenv("LLM_MODEL", "Not set"),
        "Embedding Model": os.getenv("EMBEDDING_MODEL", "Not set")
    }
    st.json(env_status)

# Tab 7: Grid 5 Live Cases
with tab7:
    st.header("🏛️ Grid 5: Live Cases Analytics")
    st.markdown("**Test the new Grid 5 Live Cases Analytics with real-time legal case data**")
    
    # Input form for Grid 5
    with st.form("grid5_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            case_id = st.text_input("Case ID", value="CASE-2024-001")
            case_context = st.text_area(
                "Case Context", 
                value="Medical negligence case involving surgical complications",
                height=100
            )
        
        with col2:
            additional_context = st.text_area(
                "Additional Context",
                value="Patient suffered complications during routine surgery",
                height=100
            )
        
        submitted = st.form_submit_button("🚀 Analyze Live Cases", type="primary")
    
    if submitted:
        st.subheader("📊 Grid 5 Analysis Results")
        
        request_data = {
            "case_id": case_id,
            "case_context": case_context,
            "additional_context": additional_context
        }
        
        try:
            with st.spinner("🔄 Analyzing live cases..."):
                response = requests.post(
                    f"{api_url}/grid/live-cases",
                    json=request_data,
                    # No timeout - let it run as long as needed
                )
            
            if response.status_code == 200:
                result = response.json()
                
                st.success(f"✅ {result['message']}")
                
                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Cases", result['total_cases'])
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
                            if case.get('url'):
                                st.markdown(f"**URL:** [View Case]({case['url']})")
                        
                        with col2:
                            score = case['similarity_score']
                            if score >= 0.9:
                                st.success(f"🎯 Similarity: {score:.1%}")
                            elif score >= 0.8:
                                st.warning(f"🔶 Similarity: {score:.1%}")
                            else:
                                st.info(f"🔵 Similarity: {score:.1%}")
                
                # Raw response
                with st.expander("📥 Raw API Response", expanded=False):
                    st.json(result)
                    
            else:
                st.error(f"❌ API Error: {response.status_code}")
                st.code(response.text)
                
        except Exception as e:
            st.error(f"❌ Error: {e}")
    
    # Quick test buttons
    st.subheader("🧪 Quick Tests")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 View Demo Cases"):
            try:
                response = requests.get(f"{api_url}/demo/cases")
                if response.status_code == 200:
                    demo_data = response.json()
                    st.success(f"✅ {demo_data['message']}")
                    st.json(demo_data['cases'])
                else:
                    st.error(f"❌ Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    with col2:
        if st.button("📊 System Status"):
            try:
                response = requests.get(f"{api_url}/system/status")
                if response.status_code == 200:
                    st.success("✅ System Status")
                    st.json(response.json())
                else:
                    st.error(f"❌ Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
