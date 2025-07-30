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
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "🤖 Individual Agents",
    "📊 Dashboard Population",
    "🚀 OPTIMIZED 3-Grid",
    "💬 Chat APIs",
    "📈 Performance Monitoring",
    "📡 Streaming APIs",
    "🔧 Advanced Testing",
    "🏛️ Grid 5: Live Cases",
    "📝 FIR Intelligence"
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

# Tab 3: OPTIMIZED 3-GRID DASHBOARD
with tab3:
    st.header("🚀 OPTIMIZED 4-GRID DASHBOARD - FIR Intelligence Enabled!")
    
    # Performance comparison banner
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⚡ Speed", "15-30s", "-75% time")
    with col2:
        st.metric("💰 Cost", "3 API calls", "-40% cost")
    with col3:
        st.metric("🎯 Value", "95%", "High relevance")
    
    st.markdown("---")
    
    # Grid explanation
    st.subheader("📋 What's in the Optimized System:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **🏛️ Grid 1: Legal Compliance**
        - Uses BNS laws + Police procedures
        - Generates actionable checklists
        - Compliance percentage tracking
        - Priority-based recommendations
        """)
    
    with col2:
        st.info("""
        **⚖️ Grid 2: BNS Laws & Severity**
        - Extracts relevant BNS sections
        - Severity classification (H/M/L)
        - Relevance scoring (0.0-1.0)
        - Legal framework mapping
        """)
    
    with col3:
        st.info("""
        **🔍 Grid 3: Live Cases Analytics**
        - Real Indian Kanoon API data
        - Advanced similarity scoring
        - Court hierarchy bonuses
        - Case type categorization
        """)
    
    st.markdown("---")
    
    # Input form
    st.subheader("🎯 Test the Optimized Dashboard")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        case_context = st.text_area(
            "Case Context",
            value="Medical malpractice case involving negligent surgery leading to patient complications. Hospital failed to follow proper protocols.",
            height=100,
            help="Describe the legal case context for analysis"
        )
        
        case_id = st.text_input(
            "Case ID", 
            value=f"OPT-{str(uuid.uuid4())[:8]}",
            help="Unique identifier for this case"
        )
    
    with col2:
        st.markdown("**🔧 Advanced Options**")
        
        user_role = st.selectbox(
            "User Role",
            ["police_officer", "legal_analyst", "compliance_officer"],
            help="Role affects response formatting"
        )
        
        jurisdiction = st.selectbox(
            "Jurisdiction",
            ["national", "state", "district"],
            help="Legal jurisdiction scope"
        )
        
        show_metadata = st.checkbox("Show Performance Metadata", value=True)
    
    # Test button
    if st.button("🚀 RUN OPTIMIZED 4-GRID DASHBOARD", type="primary", use_container_width=True):
        if case_context and case_id:
            try:
                with st.spinner("⚡ Running optimized 3-grid dashboard (15-30s)..."):
                    start_time = time.time()
                    
                    # Prepare request
                    request_data = {
                        "case_id": case_id,
                        "case_context": case_context,
                        "user_role": user_role,
                        "jurisdiction": jurisdiction
                    }
                    
                    # Call optimized endpoint
                    response = requests.post(
                        f"{api_url}/dashboard/populate-optimized",
                        json=request_data,
                        timeout=300  # 5 minutes timeout for revolutionary processing
                    )
                    
                    execution_time = time.time() - start_time
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Revolutionary Success banner
                        generation_time = result.get('generation_time', execution_time)
                        time_status = "🚀 Lightning Fast" if generation_time < 30 else "✅ Excellent" if generation_time < 60 else "⚠️ Acceptable"
                        st.success(f"✅ Revolutionary 4-Grid Dashboard completed in {execution_time:.2f}s! ({time_status})")

                        # Enhanced Performance metrics with revolutionary features
                        if show_metadata:
                            col1, col2, col3, col4, col5 = st.columns(5)
                            with col1:
                                st.metric("⏱️ Total Time", f"{execution_time:.2f}s",
                                         delta="🚀 Fast" if execution_time < 30 else "✅ Good" if execution_time < 60 else "")
                            with col2:
                                grid_count = result.get('grid_count', 4)
                                st.metric("📊 Grid Count", grid_count, delta="📝 +FIR" if grid_count >= 4 else "")
                            with col3:
                                ai_confidence = result.get('ai_confidence', 0.9)
                                confidence_delta = "🎯 High" if ai_confidence > 0.9 else "✅ Good" if ai_confidence > 0.7 else "⚠️ Low"
                                st.metric("🧠 AI Confidence", f"{ai_confidence:.1%}", delta=confidence_delta)
                            with col4:
                                cost_reduction = result.get("cost_reduction", "40%")
                                st.metric("💰 Cost Efficiency", cost_reduction, delta="🚀 Optimized")
                            with col5:
                                prompt_system = result.get('prompt_system', 'standard')
                                system_type = "🚀 Revolutionary" if 'revolutionary' in prompt_system else "⚡ Standard"
                                st.metric("🧠 AI System", system_type)

                            # Revolutionary Features Detection
                            revolutionary_features = []
                            if 'revolutionary' in result.get('prompt_system', ''):
                                revolutionary_features.append("🧠 Revolutionary Prompts")
                            if result.get('crime_type_detection'):
                                revolutionary_features.append("🎯 Crime Type Detection")
                            if 'comprehensive' in result.get('knowledge_base_utilization', ''):
                                revolutionary_features.append("📚 Knowledge Base")
                            if result.get('grid_4_fir_intelligence'):
                                revolutionary_features.append("📝 FIR Intelligence")

                            if revolutionary_features:
                                st.info(f"🚀 **Revolutionary Features Active:** {' • '.join(revolutionary_features)}")

                            # Performance Improvement Banner
                            performance_improvement = result.get('performance_improvement', '')
                            if performance_improvement:
                                st.success(f"⚡ **Performance Enhancement:** {performance_improvement}")

                            # Success metrics with enhanced display
                            success_metrics = result.get("success_metrics", {})
                            if success_metrics:
                                legal_success = success_metrics.get('legal_analysis', False)
                                cases_success = success_metrics.get('live_cases', False)
                                overall_success = success_metrics.get('overall', False)

                                success_text = []
                                success_text.append(f"Legal: {'✅' if legal_success else '❌'}")
                                success_text.append(f"Cases: {'✅' if cases_success else '❌'}")
                                success_text.append(f"Overall: {'✅' if overall_success else '❌'}")

                                success_color = "success" if overall_success else "warning"
                                if success_color == "success":
                                    st.success(f"🎯 **Success Rate:** {' • '.join(success_text)}")
                                else:
                                    st.warning(f"⚠️ **Success Rate:** {' • '.join(success_text)}")
                        
                        st.markdown("---")
                        
                        # Display results in tabs
                        grid_tab1, grid_tab2, grid_tab3, grid_tab4 = st.tabs(["🏛️ Legal Compliance", "⚖️ BNS Laws", "🔍 Live Cases", "📝 FIR Intelligence"])
                        
                        with grid_tab1:
                            st.subheader("🏛️ Grid 1: Legal Compliance - Revolutionary Analysis")
                            compliance_data = result.get("legal_compliance", "No compliance data available")

                            # Parse compliance data for revolutionary features
                            if "BNS Section" in compliance_data or "BNSS" in compliance_data or "BSA" in compliance_data:
                                st.success("🚀 **Revolutionary Legal Framework Detected:** BNS 2023, BNSS 2023, BSA 2023")

                            # Check for crime-specific analysis
                            crime_indicators = ["medical negligence", "corruption", "cyber crime", "financial fraud", "domestic violence"]
                            detected_crime = None
                            for crime in crime_indicators:
                                if crime.lower() in compliance_data.lower():
                                    detected_crime = crime
                                    break

                            if detected_crime:
                                st.info(f"🎯 **Crime-Specific Analysis:** {detected_crime.title()} compliance framework applied")

                            # Display compliance analysis
                            st.markdown("**📋 Compliance Analysis:**")
                            st.markdown(compliance_data)

                            # Extract compliance items if structured
                            compliance_lines = compliance_data.split('\n')
                            compliance_items = []
                            for line in compliance_lines:
                                if any(keyword in line.lower() for keyword in ['status:', 'priority:', 'compliance', 'requirement']):
                                    compliance_items.append(line.strip())

                            if compliance_items:
                                st.markdown("**📊 Key Compliance Points:**")
                                for item in compliance_items[:5]:  # Show top 5
                                    if item:
                                        st.write(f"• {item}")

                            # Download button
                            st.download_button(
                                "📥 Download Compliance Report",
                                data=compliance_data,
                                file_name=f"compliance_{case_id}.txt",
                                mime="text/plain"
                            )
                        
                        with grid_tab2:
                            st.subheader("⚖️ Grid 2: BNS Laws & Severity - Revolutionary Legal Intelligence")
                            laws_data = result.get("bns_laws", "No laws data available")

                            # Parse for revolutionary legal framework
                            modern_acts = ["BNS 2023", "BNSS 2023", "BSA 2023", "NDPS", "POCSO", "IT Act", "DV Act"]
                            detected_acts = []
                            for act in modern_acts:
                                if act in laws_data:
                                    detected_acts.append(act)

                            if detected_acts:
                                st.success(f"🚀 **Modern Legal Framework:** {', '.join(detected_acts)}")

                            # Extract BNS sections
                            import re
                            section_pattern = r'Section\s+(\d+[A-Za-z]*)'
                            sections = re.findall(section_pattern, laws_data, re.IGNORECASE)

                            if sections:
                                st.info(f"⚖️ **BNS Sections Identified:** {', '.join(set(sections))}")

                            # Check for severity indicators
                            severity_indicators = {
                                "High": ["murder", "death", "life imprisonment", "serious"],
                                "Medium": ["imprisonment", "fine", "punishment"],
                                "Low": ["minor", "simple", "bailable"]
                            }

                            detected_severity = []
                            for severity, keywords in severity_indicators.items():
                                if any(keyword in laws_data.lower() for keyword in keywords):
                                    detected_severity.append(severity)

                            if detected_severity:
                                severity_color = "error" if "High" in detected_severity else "warning" if "Medium" in detected_severity else "info"
                                if severity_color == "error":
                                    st.error(f"🔴 **High Severity Case:** Serious legal implications detected")
                                elif severity_color == "warning":
                                    st.warning(f"🟡 **Medium Severity Case:** Standard legal procedures apply")
                                else:
                                    st.info(f"🟢 **Low Severity Case:** Minor legal implications")

                            # Display laws analysis
                            st.markdown("**📜 Legal Analysis:**")
                            st.markdown(laws_data)

                            # Extract key legal points
                            laws_lines = laws_data.split('\n')
                            key_points = []
                            for line in laws_lines:
                                if any(keyword in line.lower() for keyword in ['section', 'punishment', 'penalty', 'imprisonment', 'applicable']):
                                    if len(line.strip()) > 20:  # Filter out short lines
                                        key_points.append(line.strip())

                            if key_points:
                                st.markdown("**🎯 Key Legal Points:**")
                                for point in key_points[:5]:  # Show top 5
                                    if point:
                                        st.write(f"• {point}")

                            # Download button
                            st.download_button(
                                "📥 Download Laws Analysis",
                                data=laws_data,
                                file_name=f"laws_{case_id}.txt",
                                mime="text/plain"
                            )
                        
                        with grid_tab3:
                            st.subheader("🔍 Grid 3: Live Cases Analytics")
                            live_cases = result.get("live_cases")
                            
                            if live_cases and live_cases.get("cases"):
                                st.success(f"Found {len(live_cases['cases'])} similar cases")
                                
                                for i, case in enumerate(live_cases["cases"][:5]):
                                    with st.expander(f"📋 Case {i+1}: {case.get('title', 'Unknown')[:100]}..."):
                                        col1, col2 = st.columns([3, 1])
                                        
                                        with col1:
                                            st.write(f"**Court:** {case.get('court', 'Unknown')}")
                                            st.write(f"**Citation:** {case.get('citation', 'N/A')}")
                                            st.write(f"**Headline:** {case.get('headline', 'N/A')}")
                                        
                                        with col2:
                                            similarity = case.get('similarity_score', 0)
                                            st.metric("Similarity", f"{similarity:.1%}")
                                            
                                            if case.get('url'):
                                                st.link_button("🔗 View Case", case['url'])
                            else:
                                st.warning("⚠️ No live cases data available (check Indian Kanoon API token)")
                        
                        with grid_tab4:
                            st.subheader("📝 Grid 4: FIR Intelligence - Revolutionary AI-Powered Analysis")
                            fir_data = result.get("grid_4_fir_intelligence", {})

                            if fir_data:
                                # FIR Intelligence Metrics
                                col1, col2, col3, col4 = st.columns(4)
                                with col1:
                                    ai_confidence = fir_data.get("ai_confidence", 0)
                                    st.metric("🧠 AI Confidence", f"{ai_confidence:.1%}")
                                with col2:
                                    sections_count = len(fir_data.get("grid_1_sections", []))
                                    st.metric("⚖️ Legal Sections", sections_count)
                                with col3:
                                    completeness_count = len(fir_data.get("grid_2_completeness", []))
                                    st.metric("📋 Completeness Items", completeness_count)
                                with col4:
                                    practices_count = len(fir_data.get("grid_3_best_practices", []))
                                    st.metric("💡 Best Practices", practices_count)

                                # Revolutionary Features Detection
                                crime_type = fir_data.get("crime_type")
                                if crime_type:
                                    st.info(f"🎯 **Crime Type Detected:** {crime_type.replace('_', ' ').title()}")

                                # FIR Intelligence Sub-tabs
                                fir_sub_tab1, fir_sub_tab2, fir_sub_tab3, fir_sub_tab4 = st.tabs([
                                    "📄 FIR Document", "⚖️ Legal Sections", "📋 Completeness", "💡 Best Practices"
                                ])

                                with fir_sub_tab1:
                                    st.markdown("**🚀 AI-Generated FIR Document:**")
                                    fir_text = fir_data.get("fir_text", "No FIR draft available.")
                                    st.code(fir_text, language="markdown")

                                    # Download FIR button
                                    st.download_button(
                                        "📥 Download FIR Document",
                                        data=fir_text,
                                        file_name=f"fir_draft_{case_id}.txt",
                                        mime="text/plain"
                                    )

                                with fir_sub_tab2:
                                    st.markdown("**⚖️ Legal Section Recommendations:**")
                                    sections = fir_data.get("grid_1_sections", [])
                                    if sections:
                                        for i, section in enumerate(sections, 1):
                                            st.write(f"{i}. {section}")
                                    else:
                                        st.info("No legal sections identified")

                                with fir_sub_tab3:
                                    st.markdown("**📋 Completeness Analysis:**")
                                    completeness = fir_data.get("grid_2_completeness", [])
                                    if completeness:
                                        # Calculate completion statistics
                                        total_items = len(completeness)
                                        completed_items = 0
                                        high_priority = 0

                                        for item in completeness:
                                            if isinstance(item, dict):
                                                if item.get("status") == "complete":
                                                    completed_items += 1
                                                if item.get("priority") == "high":
                                                    high_priority += 1

                                        # Display completion metrics
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            completion_rate = (completed_items / total_items * 100) if total_items > 0 else 0
                                            st.metric("Completion Rate", f"{completion_rate:.0f}%")
                                        with col2:
                                            st.metric("High Priority Items", high_priority)
                                        with col3:
                                            st.metric("Total Items", total_items)

                                        # Display completeness items
                                        for item in completeness:
                                            if isinstance(item, dict):
                                                field = item.get("field", "Unknown Field")
                                                status = item.get("status", "unknown")
                                                priority = item.get("priority", "medium")
                                                suggestion = item.get("suggestion", "")

                                                # Status emoji
                                                status_emoji = "✅" if status == "complete" else "⏳" if status == "incomplete" else "❌"
                                                priority_emoji = "🔴" if priority == "high" else "🟡" if priority == "medium" else "🟢"

                                                with st.expander(f"{status_emoji} {field} ({priority_emoji} {priority.title()})"):
                                                    st.write(f"**Status:** {status.title()}")
                                                    st.write(f"**Priority:** {priority.title()}")
                                                    if suggestion:
                                                        st.write(f"**Suggestion:** {suggestion}")
                                            else:
                                                st.write(f"• {item}")
                                    else:
                                        st.info("No completeness analysis available")

                                with fir_sub_tab4:
                                    st.markdown("**💡 Best Practices & Recommendations:**")
                                    practices = fir_data.get("grid_3_best_practices", [])
                                    if practices:
                                        for i, practice in enumerate(practices, 1):
                                            # Check if practice contains emoji or special formatting
                                            if any(emoji in practice for emoji in ['🏥', '👨‍⚕️', '📋', '⚖️', '💻', '🌐', '🔍', '🧪', '👶', '🛡️', '🏠']):
                                                st.markdown(f"{i}. {practice}")
                                            else:
                                                st.write(f"{i}. {practice}")
                                    else:
                                        st.info("No best practices available")

                                # Revolutionary Features Summary
                                st.markdown("---")
                                st.markdown("**🚀 Revolutionary Features Active:**")

                                revolutionary_features = []
                                if crime_type:
                                    revolutionary_features.append(f"🎯 Crime Type Detection: {crime_type.replace('_', ' ').title()}")
                                if ai_confidence > 0.8:
                                    revolutionary_features.append(f"🧠 High AI Confidence: {ai_confidence:.1%}")
                                if sections_count > 5:
                                    revolutionary_features.append(f"⚖️ Comprehensive Legal Analysis: {sections_count} sections")
                                if completeness_count > 10:
                                    revolutionary_features.append(f"📋 Detailed Completeness Check: {completeness_count} items")

                                if revolutionary_features:
                                    for feature in revolutionary_features:
                                        st.success(feature)
                                else:
                                    st.info("🔄 Standard FIR intelligence mode active")

                            else:
                                st.warning("⚠️ No FIR Intelligence data available.")
                                st.info("💡 FIR Intelligence requires case context and legal analysis to generate comprehensive results.")
                        
                        # Raw JSON view
                        with st.expander("🔍 View Raw JSON Response"):
                            st.json(result)
                    
                    else:
                        st.error(f"❌ Error {response.status_code}: {response.text}")
                        
            except Exception as e:
                st.error(f"❌ Request failed: {e}")
                st.info("💡 Make sure the backend server is running on the correct URL")
        else:
            st.warning("⚠️ Please provide both Case Context and Case ID")
    
    # Comparison with old system
    st.markdown("---")
    st.subheader("📊 Performance Comparison")
    
    comparison_data = {
        "Metric": ["Execution Time", "API Calls", "Grid Count", "Timeout Risk", "Value Relevance"],
        "Old 5-Grid System": ["75-150 seconds", "5 OpenAI + 1 Indian Kanoon", "5 grids", "High (>120s)", "60% useful"],
        "New 3-Grid System": ["15-30 seconds", "3 OpenAI + 1 Indian Kanoon", "3 grids", "Low (<60s)", "95% useful"]
    }
    
    st.table(comparison_data)

# Tab 4: Chat APIs Testing
with tab4:
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

# Tab 5: Performance Monitoring
with tab5:
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

# Tab 6: Streaming API Testing
with tab6:
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

# Tab 7: Status and Monitoring
with tab7:
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

# Tab 8: Grid 5 Live Cases
with tab8:
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

# Tab 9: FIR Intelligence Testing
with tab9:
    st.header("📝 FIR Intelligence Testing")
    st.markdown("Comprehensive testing for FIR drafting and intelligence features")

    # Create sub-tabs for different FIR testing scenarios
    fir_tab1, fir_tab2, fir_tab3, fir_tab4 = st.tabs([
        "📋 Basic FIR Draft",
        "🧠 FIR Intelligence Dashboard",
        "🔍 Scenario Testing",
        "📊 Batch Testing"
    ])

    # Tab 9.1: Basic FIR Draft Testing
    with fir_tab1:
        st.subheader("📋 Basic FIR Draft Testing")
        st.markdown("Test the basic FIR drafting endpoint with standard fields")

        with st.form("basic_fir_form"):
            col1, col2 = st.columns(2)

            with col1:
                complainant_name = st.text_input("Complainant Name", "Rahul Sharma")
                complainant_address = st.text_area("Complainant Address", "123 Main Street, Sector 15, Mumbai, Maharashtra - 400001")
                complainant_phone = st.text_input("Contact Number", "+91-9876543210")
                incident_date = st.date_input("Incident Date")
                incident_time = st.time_input("Incident Time")

            with col2:
                incident_place = st.text_input("Place of Occurrence", "Near City Park, Bandra West, Mumbai")
                police_station = st.text_input("Police Station", "Bandra Police Station")
                accused_name = st.text_input("Accused Name (if known)", "")
                accused_description = st.text_area("Accused Description", "Unknown person, approximately 25-30 years old")

            incident_description = st.text_area(
                "Incident Description",
                "The complainant was walking in the park when an unknown person snatched his mobile phone and wallet. The accused fled on a motorcycle.",
                height=100
            )
            additional_details = st.text_area("Additional Details", "CCTV cameras may have captured the incident")

            submit_basic = st.form_submit_button("🚀 Generate Basic FIR", type="primary")

        if submit_basic:
            payload = {
                "complainant_name": complainant_name,
                "complainant_address": complainant_address,
                "complainant_phone": complainant_phone,
                "accused_name": accused_name,
                "accused_description": accused_description,
                "incident_date": str(incident_date),
                "incident_time": str(incident_time),
                "incident_place": incident_place,
                "incident_description": incident_description,
                "police_station": police_station,
                "additional_details": additional_details
            }

            with st.spinner("Generating FIR..."):
                try:
                    response = requests.post(f"{api_url}/fir/draft", json=payload, timeout=300)
                    if response.status_code == 200:
                        fir_data = response.json()
                        st.success("✅ FIR Generated Successfully!")
                        st.subheader("📄 Generated FIR Document")
                        st.code(fir_data["fir_text"], language="text")

                        # Download button
                        st.download_button(
                            label="📥 Download FIR",
                            data=fir_data["fir_text"],
                            file_name=f"FIR_{complainant_name.replace(' ', '_')}_{incident_date}.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error(f"❌ Error {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"❌ Request failed: {e}")

    # Tab 9.2: FIR Intelligence Dashboard Testing
    with fir_tab2:
        st.subheader("🧠 FIR Intelligence Dashboard Testing")
        st.markdown("Test the advanced FIR intelligence features with legal analysis")

        with st.form("intelligence_fir_form"):
            col1, col2 = st.columns(2)

            with col1:
                int_complainant_name = st.text_input("Complainant Name", "Dr. Priya Patel", key="int_complainant")
                int_complainant_address = st.text_area("Complainant Address", "456 Medical Colony, Andheri East, Mumbai - 400069", key="int_address")
                int_incident_date = st.date_input("Incident Date", key="int_date")
                int_incident_time = st.time_input("Incident Time", key="int_time")
                int_incident_place = st.text_input("Place of Occurrence", "City Hospital, Operation Theater 3", key="int_place")

            with col2:
                int_police_station = st.text_input("Police Station", "Andheri Police Station", key="int_station")
                int_accused_name = st.text_input("Accused Name", "Dr. Rajesh Kumar", key="int_accused")
                int_witness_details = st.text_area("Witness Details", "Nurse Sunita Rao, Anesthesiologist Dr. Mehta", key="int_witness")

            # Predefined scenarios for testing
            scenario = st.selectbox("Select Test Scenario", [
                "Custom",
                "Medical Negligence",
                "Cyber Fraud",
                "Vehicle Accident",
                "Domestic Violence",
                "Theft/Robbery",
                "Assault Case"
            ])

            # Set default values based on scenario
            if scenario == "Medical Negligence":
                default_desc = "During a routine surgery, the accused doctor failed to follow proper medical protocols, resulting in complications and patient harm. The patient suffered additional injuries due to negligent surgical procedures."
                default_legal = "Medical negligence case involving surgical malpractice and violation of medical standards"
            elif scenario == "Cyber Fraud":
                default_desc = "The complainant received fraudulent messages claiming to be from the bank, asking for OTP and personal details. Money was transferred from the account without authorization."
                default_legal = "Cyber fraud case involving phishing and unauthorized financial transactions"
            elif scenario == "Vehicle Accident":
                default_desc = "The accused was driving rashly and hit the complainant's vehicle, causing injuries and property damage. The accused fled from the scene without providing assistance."
                default_legal = "Traffic accident case involving rash driving and hit-and-run"
            else:
                default_desc = incident_description if 'incident_description' in locals() else ""
                default_legal = ""

            int_incident_description = st.text_area(
                "Incident Description",
                default_desc,
                height=120,
                key="int_description"
            )

            int_legal_sections = st.text_area(
                "Legal Context (from dashboard)",
                default_legal,
                help="This simulates legal analysis from the dashboard grids",
                key="int_legal"
            )

            int_additional_details = st.text_area("Additional Details", key="int_additional")

            submit_intelligence = st.form_submit_button("🧠 Generate Intelligence FIR", type="primary")

        if submit_intelligence:
            fir_fields = {
                "complainant_name": int_complainant_name,
                "complainant_address": int_complainant_address,
                "incident_date": str(int_incident_date),
                "incident_time": str(int_incident_time),
                "incident_place": int_incident_place,
                "incident_description": int_incident_description,
                "police_station": int_police_station,
                "accused_name": int_accused_name,
                "witness_details": int_witness_details,
                "additional_details": int_additional_details,
                "legal_sections": int_legal_sections
            }

            payload = {"fir_fields": fir_fields}

            with st.spinner("Analyzing FIR with AI Intelligence..."):
                try:
                    start_time = time.time()
                    response = requests.post(f"{api_url}/fir/intelligence-dashboard", json=payload, timeout=300)
                    end_time = time.time()

                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"✅ FIR Intelligence Analysis Complete! ({end_time - start_time:.2f}s)")

                        # Display results in organized tabs
                        intel_tab1, intel_tab2, intel_tab3, intel_tab4, intel_tab5 = st.tabs([
                            "📄 FIR Document",
                            "⚖️ Legal Sections",
                            "✅ Completeness",
                            "💡 Best Practices",
                            "📊 Analysis Metrics"
                        ])

                        with intel_tab1:
                            st.subheader("📄 Generated FIR Document")
                            st.code(data.get("fir_text", "No FIR text available"), language="text")

                            # Download button
                            st.download_button(
                                label="📥 Download Intelligence FIR",
                                data=data.get("fir_text", ""),
                                file_name=f"Intelligence_FIR_{int_complainant_name.replace(' ', '_')}_{int_incident_date}.txt",
                                mime="text/plain"
                            )

                        with intel_tab2:
                            st.subheader("⚖️ Suggested Legal Sections")
                            sections = data.get("grid_1_sections", [])
                            if sections:
                                for section in sections:
                                    st.write(f"• {section}")
                            else:
                                st.warning("No legal sections identified")

                        with intel_tab3:
                            st.subheader("✅ Completeness Analysis")
                            completeness = data.get("grid_2_completeness", [])
                            if completeness:
                                for item in completeness:
                                    status = item.get("status", "unknown")
                                    field = item.get("field", "Unknown Field")
                                    priority = item.get("priority", "medium")

                                    if status == "complete":
                                        st.success(f"✅ {field}")
                                    elif status == "missing":
                                        st.error(f"❌ {field} - {item.get('suggestion', 'Required field')}")
                                    elif status == "incomplete":
                                        st.warning(f"⚠️ {field} - {item.get('suggestion', 'Needs improvement')}")
                                    else:
                                        st.info(f"ℹ️ {field} - {item.get('suggestion', 'Optional field')}")
                            else:
                                st.warning("No completeness data available")

                        with intel_tab4:
                            st.subheader("💡 Best Practices & Recommendations")
                            practices = data.get("grid_3_best_practices", [])
                            if practices:
                                for practice in practices:
                                    st.write(f"• {practice}")
                            else:
                                st.info("No specific recommendations for this case")

                        with intel_tab5:
                            st.subheader("📊 Analysis Metrics")
                            col1, col2, col3 = st.columns(3)

                            with col1:
                                st.metric("Generation Time", f"{data.get('generation_time', 0):.2f}s")

                            with col2:
                                confidence = data.get('ai_confidence', 0)
                                st.metric("AI Confidence", f"{confidence:.1%}")

                            with col3:
                                sections_count = len(data.get('grid_1_sections', []))
                                st.metric("Legal Sections", sections_count)

                            # Raw JSON for debugging
                            with st.expander("🔍 Raw Response Data"):
                                st.json(data)

                    else:
                        st.error(f"❌ Error {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"❌ Request failed: {e}")
                    st.info("💡 Make sure the backend server is running and accessible")

    # Tab 9.3: Scenario Testing
    with fir_tab3:
        st.subheader("🔍 Predefined Scenario Testing")
        st.markdown("Test FIR intelligence with predefined legal scenarios")

        # Predefined test scenarios
        test_scenarios = {
            "Medical Negligence": {
                "complainant_name": "Mrs. Sunita Sharma",
                "complainant_address": "789 Residential Complex, Powai, Mumbai - 400076",
                "incident_date": "2024-01-15",
                "incident_time": "14:30",
                "incident_place": "Apollo Hospital, Operation Theater 2",
                "incident_description": "During a routine appendectomy, the surgeon left a surgical instrument inside the patient's abdomen. This was discovered only after the patient experienced severe complications and required emergency surgery. The negligence caused additional pain, medical expenses, and prolonged recovery.",
                "police_station": "Powai Police Station",
                "accused_name": "Dr. Rajesh Gupta",
                "legal_sections": "Medical negligence case involving surgical malpractice under BNS Section 304A (causing death by negligence) and Section 338 (causing grievous hurt by act endangering life)",
                "expected_sections": ["BNS 304A", "BNS 338", "BNS 336"]
            },
            "Cyber Fraud": {
                "complainant_name": "Mr. Amit Patel",
                "complainant_address": "456 Tech Park, Whitefield, Bangalore - 560066",
                "incident_date": "2024-01-20",
                "incident_time": "19:45",
                "incident_place": "Online/Digital Platform",
                "incident_description": "The complainant received a call from someone claiming to be from his bank, asking for OTP for 'security verification'. After sharing the OTP, Rs. 2,50,000 was transferred from his account to unknown accounts. The fraudster used social engineering techniques to gain trust.",
                "police_station": "Whitefield Cyber Crime Police Station",
                "accused_name": "Unknown (Phone number: +91-9876543210)",
                "legal_sections": "Cyber fraud case involving phishing and unauthorized financial transactions under IT Act and BNS provisions",
                "expected_sections": ["BNS 420", "BNS 415", "IT Act 66C", "IT Act 66D"]
            },
            "Vehicle Accident": {
                "complainant_name": "Mr. Ravi Kumar",
                "complainant_address": "123 Highway Residency, Gurgaon - 122001",
                "incident_date": "2024-01-25",
                "incident_time": "08:15",
                "incident_place": "NH-8 Highway, near Gurgaon Toll Plaza",
                "incident_description": "The accused was driving a truck at high speed and overtaking rashly. He hit the complainant's car from behind, causing the car to overturn. The complainant suffered multiple injuries and the vehicle was completely damaged. The accused fled from the scene without providing assistance.",
                "police_station": "Highway Police Station",
                "accused_name": "Unknown truck driver (Vehicle: HR-55-AB-1234)",
                "legal_sections": "Traffic accident case involving rash driving and hit-and-run under motor vehicle laws and BNS",
                "expected_sections": ["BNS 279", "BNS 337", "BNS 338", "Motor Vehicle Act"]
            }
        }

        selected_scenario = st.selectbox("Select Test Scenario", list(test_scenarios.keys()))

        if st.button(f"🧪 Test {selected_scenario} Scenario", type="primary"):
            scenario_data = test_scenarios[selected_scenario]

            # Prepare payload
            fir_fields = {k: v for k, v in scenario_data.items() if k != "expected_sections"}
            payload = {"fir_fields": fir_fields}

            with st.spinner(f"Testing {selected_scenario} scenario..."):
                try:
                    start_time = time.time()
                    response = requests.post(f"{api_url}/fir/intelligence-dashboard", json=payload, timeout=300)
                    end_time = time.time()

                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"✅ {selected_scenario} Test Complete! ({end_time - start_time:.2f}s)")

                        # Validation against expected results
                        expected_sections = scenario_data.get("expected_sections", [])
                        actual_sections = data.get("grid_1_sections", [])

                        # Calculate accuracy
                        if expected_sections:
                            matched_sections = []
                            for expected in expected_sections:
                                for actual in actual_sections:
                                    if expected.lower() in actual.lower():
                                        matched_sections.append(expected)
                                        break

                            accuracy = len(matched_sections) / len(expected_sections) * 100

                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Section Accuracy", f"{accuracy:.1f}%")
                            with col2:
                                st.metric("AI Confidence", f"{data.get('ai_confidence', 0):.1%}")
                            with col3:
                                st.metric("Processing Time", f"{data.get('generation_time', 0):.2f}s")

                        # Display comparison
                        comp_col1, comp_col2 = st.columns(2)

                        with comp_col1:
                            st.subheader("Expected Sections")
                            for section in expected_sections:
                                st.write(f"• {section}")

                        with comp_col2:
                            st.subheader("AI Suggested Sections")
                            for section in actual_sections:
                                st.write(f"• {section}")

                        # Show full results
                        with st.expander("📄 View Complete FIR"):
                            st.code(data.get("fir_text", ""), language="text")

                        with st.expander("📊 Detailed Analysis"):
                            st.json(data)

                    else:
                        st.error(f"❌ Error {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"❌ Test failed: {e}")

    # Tab 9.4: Batch Testing
    with fir_tab4:
        st.subheader("📊 Batch Testing & Performance Analysis")
        st.markdown("Run multiple FIR tests to analyze system performance and consistency")

        col1, col2 = st.columns(2)

        with col1:
            batch_size = st.number_input("Number of Tests", min_value=1, max_value=10, value=3)
            test_type = st.selectbox("Test Type", ["All Scenarios", "Random Variations", "Stress Test"])

        with col2:
            include_timing = st.checkbox("Include Performance Metrics", value=True)
            include_validation = st.checkbox("Include Accuracy Validation", value=True)

        if st.button("🚀 Run Batch Tests", type="primary"):
            results = []
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Define test cases for batch testing
            batch_scenarios = [
                {
                    "name": "Medical Case",
                    "fir_fields": {
                        "complainant_name": "Test Patient",
                        "incident_description": "Medical negligence during surgery causing patient harm",
                        "legal_sections": "Medical malpractice case with surgical complications"
                    }
                },
                {
                    "name": "Cyber Crime",
                    "fir_fields": {
                        "complainant_name": "Test Victim",
                        "incident_description": "Online fraud through phishing and unauthorized transactions",
                        "legal_sections": "Cyber fraud case involving digital deception"
                    }
                },
                {
                    "name": "Traffic Accident",
                    "fir_fields": {
                        "complainant_name": "Test Driver",
                        "incident_description": "Vehicle accident due to rash driving and negligence",
                        "legal_sections": "Traffic violation case with injury and property damage"
                    }
                }
            ]

            for i in range(batch_size):
                scenario = batch_scenarios[i % len(batch_scenarios)]
                status_text.text(f"Running test {i+1}/{batch_size}: {scenario['name']}")

                try:
                    start_time = time.time()
                    response = requests.post(
                        f"{api_url}/fir/intelligence-dashboard",
                        json={"fir_fields": scenario["fir_fields"]},
                        timeout=300
                    )
                    end_time = time.time()

                    if response.status_code == 200:
                        data = response.json()
                        results.append({
                            "test_name": scenario["name"],
                            "success": True,
                            "response_time": end_time - start_time,
                            "ai_confidence": data.get("ai_confidence", 0),
                            "sections_count": len(data.get("grid_1_sections", [])),
                            "completeness_score": len([c for c in data.get("grid_2_completeness", []) if c.get("status") == "complete"]),
                            "practices_count": len(data.get("grid_3_best_practices", []))
                        })
                    else:
                        results.append({
                            "test_name": scenario["name"],
                            "success": False,
                            "error": f"HTTP {response.status_code}",
                            "response_time": end_time - start_time
                        })

                except Exception as e:
                    results.append({
                        "test_name": scenario["name"],
                        "success": False,
                        "error": str(e),
                        "response_time": 0
                    })

                progress_bar.progress((i + 1) / batch_size)

            status_text.text("Batch testing complete!")

            # Display results
            st.subheader("📊 Batch Test Results")

            # Summary metrics
            successful_tests = [r for r in results if r.get("success", False)]
            success_rate = len(successful_tests) / len(results) * 100
            avg_response_time = sum(r.get("response_time", 0) for r in successful_tests) / len(successful_tests) if successful_tests else 0
            avg_confidence = sum(r.get("ai_confidence", 0) for r in successful_tests) / len(successful_tests) if successful_tests else 0

            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

            with metric_col1:
                st.metric("Success Rate", f"{success_rate:.1f}%")
            with metric_col2:
                st.metric("Avg Response Time", f"{avg_response_time:.2f}s")
            with metric_col3:
                st.metric("Avg AI Confidence", f"{avg_confidence:.1%}")
            with metric_col4:
                st.metric("Total Tests", len(results))

            # Detailed results table
            st.subheader("📋 Detailed Results")
            for i, result in enumerate(results):
                with st.expander(f"Test {i+1}: {result['test_name']} - {'✅ Success' if result.get('success') else '❌ Failed'}"):
                    if result.get("success"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Response Time:** {result.get('response_time', 0):.2f}s")
                            st.write(f"**AI Confidence:** {result.get('ai_confidence', 0):.1%}")
                        with col2:
                            st.write(f"**Legal Sections:** {result.get('sections_count', 0)}")
                            st.write(f"**Complete Fields:** {result.get('completeness_score', 0)}")
                            st.write(f"**Best Practices:** {result.get('practices_count', 0)}")
                    else:
                        st.error(f"Error: {result.get('error', 'Unknown error')}")

            # Export results
            if st.button("📥 Export Results as JSON"):
                st.download_button(
                    label="Download Test Results",
                    data=json.dumps(results, indent=2),
                    file_name=f"fir_batch_test_results_{time.strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
