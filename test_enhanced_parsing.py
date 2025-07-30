#!/usr/bin/env python3
"""
Test Enhanced API Tester Parsing for Revolutionary Features
"""

import requests
import json
import time

def test_enhanced_parsing():
    """Test the enhanced parsing features in the optimized dashboard"""
    print("🚀 TESTING ENHANCED API TESTER PARSING")
    print("=" * 80)
    
    # Test case that should trigger revolutionary features
    test_case = {
        "case_id": "ENHANCED-PARSE-001",
        "case_context": "Medical malpractice case involving negligent surgery leading to patient complications. Hospital failed to follow proper protocols during cardiac surgery."
    }
    
    print(f"📝 Test Case: {test_case['case_context']}")
    print(f"🎯 Expected Features:")
    print(f"   - Crime Type Detection: medical_negligence")
    print(f"   - Revolutionary Prompts: BNS 2023, BNSS 2023, BSA 2023")
    print(f"   - FIR Intelligence: Comprehensive analysis")
    print(f"   - Legal Sections: Medical-specific BNS sections")
    
    try:
        print(f"\n🔄 Calling optimized dashboard endpoint...")
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:8001/dashboard/populate-optimized",
            json=test_case,
            timeout=120
        )
        
        execution_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response received in {execution_time:.2f}s")
            
            # Test Revolutionary Features Detection
            print(f"\n🚀 REVOLUTIONARY FEATURES ANALYSIS:")
            print("=" * 60)
            
            # 1. Prompt System Detection
            prompt_system = result.get('prompt_system', 'standard')
            if 'revolutionary' in prompt_system:
                print(f"✅ Revolutionary Prompts: {prompt_system}")
            else:
                print(f"⚠️ Standard Prompts: {prompt_system}")
            
            # 2. Crime Type Detection
            crime_detection = result.get('crime_type_detection')
            if crime_detection:
                print(f"✅ Crime Type Detection: {crime_detection}")
            else:
                print(f"⚠️ No crime type detection data")
            
            # 3. Knowledge Base Utilization
            knowledge_base = result.get('knowledge_base_utilization', '')
            if 'comprehensive' in knowledge_base:
                print(f"✅ Comprehensive Knowledge Base: {knowledge_base}")
            else:
                print(f"⚠️ Standard Knowledge Base: {knowledge_base}")
            
            # 4. Performance Metrics
            generation_time = result.get('generation_time', 0)
            ai_confidence = result.get('ai_confidence', 0)
            print(f"📊 Performance: {generation_time:.2f}s, AI Confidence: {ai_confidence:.1%}")
            
            # Test Legal Compliance Parsing
            print(f"\n🏛️ LEGAL COMPLIANCE PARSING:")
            print("=" * 60)
            
            compliance_data = result.get('legal_compliance', '')
            
            # Check for modern legal framework
            modern_frameworks = ['BNS 2023', 'BNSS 2023', 'BSA 2023']
            detected_frameworks = [fw for fw in modern_frameworks if fw in compliance_data]
            if detected_frameworks:
                print(f"✅ Modern Legal Framework: {', '.join(detected_frameworks)}")
            else:
                print(f"⚠️ No modern framework detected in compliance")
            
            # Check for crime-specific analysis
            crime_indicators = ['medical negligence', 'medical malpractice', 'hospital', 'surgery']
            detected_crimes = [crime for crime in crime_indicators if crime.lower() in compliance_data.lower()]
            if detected_crimes:
                print(f"✅ Crime-Specific Analysis: {', '.join(detected_crimes)}")
            else:
                print(f"⚠️ No crime-specific indicators found")
            
            # Test BNS Laws Parsing
            print(f"\n⚖️ BNS LAWS PARSING:")
            print("=" * 60)
            
            laws_data = result.get('bns_laws', '')
            
            # Extract BNS sections
            import re
            section_pattern = r'Section\s+(\d+[A-Za-z]*)'
            sections = re.findall(section_pattern, laws_data, re.IGNORECASE)
            if sections:
                print(f"✅ BNS Sections Found: {', '.join(set(sections))}")
            else:
                print(f"⚠️ No BNS sections detected")
            
            # Check for severity indicators
            severity_high = any(word in laws_data.lower() for word in ['murder', 'death', 'life imprisonment'])
            severity_medium = any(word in laws_data.lower() for word in ['imprisonment', 'fine', 'punishment'])
            severity_low = any(word in laws_data.lower() for word in ['minor', 'simple', 'bailable'])
            
            if severity_high:
                print(f"🔴 High Severity Case Detected")
            elif severity_medium:
                print(f"🟡 Medium Severity Case Detected")
            elif severity_low:
                print(f"🟢 Low Severity Case Detected")
            else:
                print(f"⚠️ No severity indicators found")
            
            # Test Live Cases Parsing
            print(f"\n🔍 LIVE CASES PARSING:")
            print("=" * 60)
            
            live_cases = result.get('live_cases', {})
            if live_cases:
                status = live_cases.get('status', 'unknown')
                total_cases = live_cases.get('total_cases', 0)
                crime_type = live_cases.get('crime_type', 'unknown')
                
                print(f"✅ Live Cases Status: {status}")
                print(f"📊 Total Cases Found: {total_cases}")
                print(f"🎯 Crime Type: {crime_type}")
                
                cases = live_cases.get('cases', [])
                if cases:
                    print(f"📋 Sample Cases:")
                    for i, case in enumerate(cases[:3], 1):
                        title = case.get('title', 'Unknown')[:50]
                        similarity = case.get('similarity_score', 0)
                        print(f"   {i}. {title}... (Similarity: {similarity:.1%})")
            else:
                print(f"⚠️ No live cases data available")
            
            # Test FIR Intelligence Parsing
            print(f"\n📝 FIR INTELLIGENCE PARSING:")
            print("=" * 60)
            
            fir_data = result.get('grid_4_fir_intelligence', {})
            if fir_data:
                ai_confidence = fir_data.get('ai_confidence', 0)
                sections_count = len(fir_data.get('grid_1_sections', []))
                completeness_count = len(fir_data.get('grid_2_completeness', []))
                practices_count = len(fir_data.get('grid_3_best_practices', []))
                
                print(f"✅ FIR AI Confidence: {ai_confidence:.1%}")
                print(f"📊 Legal Sections: {sections_count}")
                print(f"📋 Completeness Items: {completeness_count}")
                print(f"💡 Best Practices: {practices_count}")
                
                # Check for crime-specific FIR features
                fir_text = fir_data.get('fir_text', '')
                if 'medical' in fir_text.lower() or 'hospital' in fir_text.lower():
                    print(f"✅ Medical-Specific FIR Content Detected")
                
                # Check completeness structure
                completeness = fir_data.get('grid_2_completeness', [])
                if completeness and isinstance(completeness[0], dict):
                    print(f"✅ Structured Completeness Analysis Available")
                    
                    # Count completion status
                    completed = sum(1 for item in completeness if isinstance(item, dict) and item.get('status') == 'complete')
                    total = len(completeness)
                    completion_rate = (completed / total * 100) if total > 0 else 0
                    print(f"📈 Completion Rate: {completion_rate:.0f}% ({completed}/{total})")
                else:
                    print(f"⚠️ Basic completeness format")
            else:
                print(f"⚠️ No FIR intelligence data available")
            
            # Overall Assessment
            print(f"\n🎯 OVERALL ASSESSMENT:")
            print("=" * 60)
            
            revolutionary_score = 0
            total_features = 5
            
            if 'revolutionary' in prompt_system:
                revolutionary_score += 1
                print(f"✅ Revolutionary Prompts Active")
            
            if detected_frameworks:
                revolutionary_score += 1
                print(f"✅ Modern Legal Framework Detected")
            
            if detected_crimes:
                revolutionary_score += 1
                print(f"✅ Crime-Specific Analysis Active")
            
            if sections:
                revolutionary_score += 1
                print(f"✅ BNS Section Extraction Working")
            
            if fir_data and ai_confidence > 0.5:
                revolutionary_score += 1
                print(f"✅ FIR Intelligence Functional")
            
            revolutionary_percentage = (revolutionary_score / total_features) * 100
            
            if revolutionary_percentage >= 80:
                print(f"\n🚀 EXCELLENT: {revolutionary_percentage:.0f}% revolutionary features active!")
                print(f"   Enhanced API Tester parsing will work perfectly!")
            elif revolutionary_percentage >= 60:
                print(f"\n✅ GOOD: {revolutionary_percentage:.0f}% revolutionary features active!")
                print(f"   Enhanced API Tester parsing will work well!")
            else:
                print(f"\n⚠️ BASIC: {revolutionary_percentage:.0f}% revolutionary features active!")
                print(f"   Enhanced API Tester will show basic parsing!")
            
        else:
            print(f"❌ Request failed: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    print("🔍 Testing enhanced API tester parsing capabilities...")
    test_enhanced_parsing()
    print(f"\n🎉 Test complete! Check the Streamlit app at http://localhost:8502")
    print(f"💡 Navigate to 'OPTIMIZED 4-GRID DASHBOARD' tab to see enhanced parsing!")
