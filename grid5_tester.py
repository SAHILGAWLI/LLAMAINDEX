# Grid 5 Testing Interface Addition
# Add this to the end of api_tester.py after the existing tabs

# Tab 7: Grid 5 Live Cases Analytics Testing
with tab7:
    st.header("🏛️ Grid 5: Live Cases Analytics Testing")
    
    st.info("📚 This tab tests the advanced Grid 5 functionality that integrates with Indian Kanoon API for real-time legal case analysis.")
    
    # Environment check for Indian Kanoon
    st.subheader("🔧 Indian Kanoon API Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        ik_token_status = "✅ Set" if os.getenv("INDIAN_KANOON_API_TOKEN") else "❌ Missing"
        st.metric("API Token", ik_token_status)
        
        ik_base_url = os.getenv("INDIAN_KANOON_BASE_URL", "https://api.indiankanoon.org")
        st.metric("Base URL", ik_base_url)
    
    with col2:
        max_cases = os.getenv("GRID5_MAX_CASES", "20")
        st.metric("Max Cases", max_cases)
        
        cache_ttl = os.getenv("GRID5_CACHE_TTL", "3600")
        st.metric("Cache TTL", f"{cache_ttl}s")
    
    if not os.getenv("INDIAN_KANOON_API_TOKEN"):
        st.warning("⚠️ Indian Kanoon API token not configured. Please add INDIAN_KANOON_API_TOKEN to your .env file to test Grid 5 functionality.")
        st.code("INDIAN_KANOON_API_TOKEN=your_token_here", language="bash")
    
    st.markdown("---")
    
    # Test parameters
    st.subheader("📝 Test Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        grid5_case_context = st.text_area(
            "Case Context for Live Cases Search:",
            value="Medical negligence case involving surgical malpractice during cardiac surgery. Patient suffered complications due to improper procedure. Seeking similar cases under BNS Section 304A for precedent analysis.",
            height=120,
            key="grid5_context"
        )
        
        additional_context = st.text_area(
            "Additional Legal Context (Optional):",
            value="BNS Section 304A, medical malpractice, surgical negligence, cardiac surgery complications",
            height=80,
            key="grid5_additional"
        )
    
    with col2:
        st.info("🎯 **Grid 5 Features:**\n\n• Real-time case search from Indian Kanoon\n• AI-powered similarity analysis\n• Citation network analysis\n• Case outcome prediction\n• Strategic recommendations\n• Court performance metrics")
        
        test_mode = st.radio(
            "Test Mode:",
            ["🔍 Individual Grid 5 Test", "📊 Enhanced Dashboard (All Grids + Grid 5)"],
            help="Individual: Test only Grid 5. Enhanced: Test complete dashboard with Grid 5 integration."
        )
    
    st.markdown("---")
    
    # Individual Grid 5 Testing
    if test_mode == "🔍 Individual Grid 5 Test":
        st.subheader("🔍 Individual Grid 5 Testing")
        
        if st.button("🚀 Test Grid 5: Live Cases Analytics", type="primary"):
            if not os.getenv("INDIAN_KANOON_API_TOKEN"):
                st.error("❌ Cannot test Grid 5 without Indian Kanoon API token. Please configure INDIAN_KANOON_API_TOKEN in your .env file.")
            else:
                try:
                    with st.spinner("🔍 Searching Indian Kanoon database for relevant cases..."):
                        start_time = time.time()
                        
                        response = requests.post(
                            f"{api_url}/grid/live-cases",
                            json={
                                "case_context": grid5_case_context,
                                "additional_context": additional_context
                            },
                            timeout=60  # Longer timeout for Grid 5
                        )
                        
                        end_time = time.time()
                    
                    if response.status_code == 200:
                        grid5_data = response.json()
                        st.success(f"✅ Grid 5 analysis completed in {end_time - start_time:.2f}s")
                        
                        # Display results in organized tabs
                        result_tab1, result_tab2, result_tab3, result_tab4 = st.tabs([
                            "📚 Live Cases", "📈 Analytics", "🔗 Citations", "🎯 Insights"
                        ])
                        
                        with result_tab1:
                            st.subheader(f"📚 Live Cases Found: {grid5_data.get('total_found', 0)}")
                            
                            live_cases = grid5_data.get('live_cases', [])
                            for i, case in enumerate(live_cases[:5]):  # Show top 5 cases
                                with st.expander(f"Case {i+1}: {case.get('title', 'Unknown')[:100]}..."):
                                    col_case1, col_case2 = st.columns(2)
                                    
                                    with col_case1:
                                        st.write(f"**Court:** {case.get('court', 'Unknown')}")
                                        st.write(f"**Date:** {case.get('date', 'Unknown')}")
                                        st.write(f"**Similarity Score:** {case.get('similarity_score', 0):.2%}")
                                        st.write(f"**BNS Sections:** {', '.join(case.get('bns_sections', []))}")
                                    
                                    with col_case2:
                                        st.write(f"**Outcome:** {case.get('case_outcome', 'Unknown')}")
                                        if case.get('indian_kanoon_url'):
                                            st.markdown(f"[View on Indian Kanoon]({case['indian_kanoon_url']})")
                                        st.write(f"**Summary:** {case.get('summary', 'No summary available')[:200]}...")
                        
                        with result_tab2:
                            st.subheader("📈 Case Analytics")
                            
                            case_analytics = grid5_data.get('case_analytics', {})
                            if case_analytics:
                                col_analytics1, col_analytics2 = st.columns(2)
                                
                                with col_analytics1:
                                    conviction_rate = case_analytics.get('conviction_rate')
                                    if conviction_rate is not None:
                                        st.metric("Conviction Rate", f"{conviction_rate:.1%}")
                                    
                                    st.write("**Success Patterns:**")
                                    for pattern in case_analytics.get('success_patterns', []):
                                        st.write(f"• {pattern}")
                                
                                with col_analytics2:
                                    st.write("**Risk Factors:**")
                                    for risk in case_analytics.get('risk_factors', []):
                                        st.write(f"⚠️ {risk}")
                                    
                                    st.write(f"**Legal Trends:** {case_analytics.get('legal_trends', 'No trends identified')}")
                            else:
                                st.info("No case analytics available")
                        
                        with result_tab3:
                            st.subheader("🔗 Citation Network Analysis")
                            
                            citation_network = grid5_data.get('citation_network', {})
                            if citation_network:
                                col_cite1, col_cite2, col_cite3 = st.columns(3)
                                
                                with col_cite1:
                                    st.metric("Citation Count", citation_network.get('citation_count', 0))
                                
                                with col_cite2:
                                    st.metric("Authority Score", f"{citation_network.get('authority_score', 0):.1f}/10")
                                
                                with col_cite3:
                                    st.metric("Precedent Strength", citation_network.get('precedent_strength', 'Unknown'))
                            else:
                                st.info("No citation network data available")
                        
                        with result_tab4:
                            st.subheader("🎯 Legal Insights & Recommendations")
                            
                            legal_insights = grid5_data.get('legal_insights', '')
                            if legal_insights:
                                st.write(legal_insights)
                            
                            strategic_recommendations = grid5_data.get('strategic_recommendations', [])
                            if strategic_recommendations:
                                st.write("**Strategic Recommendations:**")
                                for rec in strategic_recommendations:
                                    st.write(f"• {rec}")
                            
                            # Metadata
                            st.subheader("📄 Search Metadata")
                            metadata = {
                                "Search Query": grid5_data.get('search_query', 'N/A'),
                                "API Calls Made": grid5_data.get('api_calls_made', 0),
                                "Generation Time": f"{grid5_data.get('generation_time', 0):.2f}s",
                                "Context Summary": grid5_data.get('context_summary', 'N/A')
                            }
                            st.json(metadata)
                    
                    elif response.status_code == 503:
                        st.error("❌ Grid 5 service unavailable. Please check Indian Kanoon API configuration.")
                        st.code(response.text)
                    else:
                        st.error(f"❌ Grid 5 test failed with status {response.status_code}")
                        st.code(response.text)
                        
                except Exception as e:
                    st.error(f"❌ Grid 5 test failed: {e}")
    
    # Enhanced Dashboard Testing
    else:
        st.subheader("📊 Enhanced Dashboard Testing (All Grids + Grid 5)")
        
        case_id_grid5 = st.text_input("Case ID:", value="GRID5-TEST-001", key="grid5_case_id")
        
        if st.button("🚀 Test Enhanced Dashboard with Grid 5", type="primary"):
            if not os.getenv("INDIAN_KANOON_API_TOKEN"):
                st.warning("⚠️ Grid 5 will be skipped due to missing Indian Kanoon API token. Testing Grids 1-4 only.")
            
            try:
                with st.spinner("🔍 Running enhanced dashboard analysis with Grid 5..."):
                    start_time = time.time()
                    
                    response = requests.post(
                        f"{api_url}/dashboard/populate-with-grid5",
                        json={
                            "case_id": case_id_grid5,
                            "case_context": grid5_case_context
                        },
                        timeout=120  # Extended timeout for full dashboard
                    )
                    
                    end_time = time.time()
                
                if response.status_code == 200:
                    dashboard_data = response.json()
                    st.success(f"✅ Enhanced dashboard completed in {end_time - start_time:.2f}s")
                    
                    # Display all grids
                    grid_tab1, grid_tab2, grid_tab3, grid_tab4, grid_tab5, grid_meta = st.tabs([
                        "⚖️ Grid 1", "📜 Grid 2", "📄 Grid 3", "📈 Grid 4", "🏛️ Grid 5", "📊 Metadata"
                    ])
                    
                    with grid_tab1:
                        st.subheader("⚖️ Grid 1: Compliance")
                        st.json(dashboard_data.get("grid_1_compliance", {}))
                    
                    with grid_tab2:
                        st.subheader("📜 Grid 2: Laws")
                        st.json(dashboard_data.get("grid_2_laws", {}))
                    
                    with grid_tab3:
                        st.subheader("📄 Grid 3: Documents")
                        st.json(dashboard_data.get("grid_3_documents", {}))
                    
                    with grid_tab4:
                        st.subheader("📈 Grid 4: Cases")
                        st.json(dashboard_data.get("grid_4_cases", {}))
                    
                    with grid_tab5:
                        st.subheader("🏛️ Grid 5: Live Cases Analytics")
                        grid5_data = dashboard_data.get("grid_5_live_cases")
                        if grid5_data:
                            st.json(grid5_data)
                            
                            # Quick stats
                            col_stat1, col_stat2, col_stat3 = st.columns(3)
                            with col_stat1:
                                st.metric("Live Cases Found", grid5_data.get('total_found', 0))
                            with col_stat2:
                                st.metric("API Calls Made", grid5_data.get('api_calls_made', 0))
                            with col_stat3:
                                conviction_rate = grid5_data.get('case_analytics', {}).get('conviction_rate')
                                if conviction_rate is not None:
                                    st.metric("Conviction Rate", f"{conviction_rate:.1%}")
                        else:
                            error_msg = dashboard_data.get('error_message', 'Grid 5 data not available')
                            st.warning(f"⚠️ {error_msg}")
                    
                    with grid_meta:
                        st.subheader("📊 Enhanced Dashboard Metadata")
                        metadata = {
                            "Generation Time": f"{dashboard_data.get('generation_time', 0):.2f}s",
                            "AI Confidence": f"{dashboard_data.get('ai_confidence', 0):.1%}",
                            "Total API Calls": dashboard_data.get('total_api_calls', 0),
                            "Grid 5 Status": "Available" if dashboard_data.get('grid_5_live_cases') else "Unavailable",
                            "Error Message": dashboard_data.get('error_message', 'None')
                        }
                        st.json(metadata)
                
                else:
                    st.error(f"❌ Enhanced dashboard test failed with status {response.status_code}")
                    st.code(response.text)
                    
            except Exception as e:
                st.error(f"❌ Enhanced dashboard test failed: {e}")
