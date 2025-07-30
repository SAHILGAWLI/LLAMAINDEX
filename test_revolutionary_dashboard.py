#!/usr/bin/env python3
"""
Test Revolutionary Dashboard with Enhanced Prompts
"""

import requests
import json
import time

def test_revolutionary_dashboard():
    """Test the revolutionary /dashboard/populate-optimized endpoint"""
    print("🚀 TESTING REVOLUTIONARY DASHBOARD")
    print("=" * 60)
    
    test_cases = [
        {
            "name": "🚫 Drug Crime Test",
            "case_id": "REV-DRUG-001",
            "case_context": "Accused was found selling illegal substances including charas and ganja near a school. Police recovered 500 grams of narcotic drugs from his possession during a raid."
        },
        {
            "name": "👶 Child Protection Test", 
            "case_id": "REV-CHILD-001",
            "case_context": "Inappropriate behavior and sexual assault against a 12-year-old minor child by the accused teacher in the school premises."
        },
        {
            "name": "💻 Cyber Crime Test",
            "case_id": "REV-CYBER-001", 
            "case_context": "Online fraud through fake banking website where accused stole credit card details and transferred money from victim's account using phishing techniques."
        },
        {
            "name": "🏠 Domestic Violence Test",
            "case_id": "REV-DV-001",
            "case_context": "Husband physically assaulted wife and demanded additional dowry money. Victim suffered injuries and was denied access to household resources."
        },
        {
            "name": "🔄 Medical Negligence Test",
            "case_id": "REV-MED-001",
            "case_context": "Medical negligence during surgery where doctor failed to follow proper protocols, resulting in patient complications and additional harm."
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*20} TEST {i}/{len(test_cases)} {'='*20}")
        print(f"🧪 {test_case['name']}")
        print("=" * 60)
        print(f"📝 Case Context: {test_case['case_context']}")
        
        payload = {
            "case_id": test_case["case_id"],
            "case_context": test_case["case_context"]
        }
        
        try:
            print("🔄 Sending request to revolutionary dashboard endpoint...")
            start_time = time.time()
            
            response = requests.post(
                "http://localhost:8001/dashboard/populate-optimized",
                json=payload,
                timeout=300  # 5 minutes timeout for revolutionary processing
            )
            
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ Response received in {end_time - start_time:.2f}s")
                
                # Check if revolutionary features are working
                revolutionary_features = []
                
                # Check for crime-type detection
                if "crime_type" in str(data).lower():
                    revolutionary_features.append("Crime Type Detection")
                
                # Check for specialized sections
                legal_compliance = data.get('legal_compliance', '')
                if any(term in legal_compliance.lower() for term in ['ndps', 'pocso', 'it act', 'dv act']):
                    revolutionary_features.append("Specialized Acts Integration")
                
                # Check for enhanced confidence
                ai_confidence = data.get('ai_confidence', 0)
                if ai_confidence > 0.9:
                    revolutionary_features.append("High AI Confidence")
                
                # Check for performance improvement
                performance_improvement = data.get('performance_improvement', '')
                if 'revolutionary' in performance_improvement.lower():
                    revolutionary_features.append("Revolutionary Performance")
                
                print(f"🧠 AI Confidence: {ai_confidence:.1%}")
                print(f"⏱️ Generation Time: {data.get('generation_time', 0):.2f}s")
                print(f"🚀 Revolutionary Features: {len(revolutionary_features)}/4")
                
                for feature in revolutionary_features:
                    print(f"   ✅ {feature}")
                
                # Check grid content
                print(f"\n📊 Grid Analysis:")
                print(f"   🏛️ Legal Compliance: {len(str(legal_compliance))} chars")
                
                bns_laws = data.get('bns_laws', '')
                print(f"   ⚖️ BNS Laws: {len(str(bns_laws))} chars")
                
                live_cases = data.get('live_cases', {})
                cases_count = live_cases.get('total_cases', 0) if isinstance(live_cases, dict) else 0
                print(f"   🏛️ Live Cases: {cases_count} cases")
                
                fir_intelligence = data.get('grid_4_fir_intelligence', {})
                if fir_intelligence:
                    print(f"   📝 FIR Intelligence: Enhanced")
                
                success = ai_confidence > 0.7 and len(revolutionary_features) >= 2
                results.append({
                    "test": test_case["name"],
                    "success": success,
                    "ai_confidence": ai_confidence,
                    "generation_time": data.get('generation_time', 0),
                    "revolutionary_features": len(revolutionary_features)
                })
                
                print(f"   {'✅ SUCCESS' if success else '⚠️ PARTIAL'}: Revolutionary dashboard test")
                
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                results.append({
                    "test": test_case["name"],
                    "success": False,
                    "ai_confidence": 0,
                    "generation_time": 0,
                    "revolutionary_features": 0
                })
                
        except Exception as e:
            print(f"❌ Test failed: {e}")
            results.append({
                "test": test_case["name"],
                "success": False,
                "ai_confidence": 0,
                "generation_time": 0,
                "revolutionary_features": 0
            })
        
        # Wait between tests
        if i < len(test_cases):
            print("\n⏳ Waiting 5 seconds before next test...")
            time.sleep(5)
    
    # Final summary
    print("\n" + "="*80)
    print("📊 REVOLUTIONARY DASHBOARD TEST RESULTS")
    print("="*80)
    
    successful_tests = sum(1 for r in results if r["success"])
    total_tests = len(results)
    success_rate = (successful_tests / total_tests) * 100
    
    avg_confidence = sum(r["ai_confidence"] for r in results) / len(results)
    avg_time = sum(r["generation_time"] for r in results) / len(results)
    avg_features = sum(r["revolutionary_features"] for r in results) / len(results)
    
    for result in results:
        status = "✅ PASSED" if result["success"] else "❌ FAILED"
        print(f"   {status}: {result['test']}")
        print(f"      🧠 AI Confidence: {result['ai_confidence']:.1%}")
        print(f"      ⏱️ Time: {result['generation_time']:.2f}s")
        print(f"      🚀 Revolutionary Features: {result['revolutionary_features']}/4")
    
    print(f"\n🎯 OVERALL RESULTS:")
    print(f"   Successful Tests: {successful_tests}/{total_tests}")
    print(f"   Success Rate: {success_rate:.1f}%")
    print(f"   Average AI Confidence: {avg_confidence:.1%}")
    print(f"   Average Generation Time: {avg_time:.2f}s")
    print(f"   Average Revolutionary Features: {avg_features:.1f}/4")
    
    if success_rate >= 80:
        print(f"   🎉 EXCELLENT: Revolutionary dashboard is working great!")
    elif success_rate >= 60:
        print(f"   ✅ GOOD: Most features working, some fine-tuning needed")
    else:
        print(f"   ⚠️ NEEDS WORK: Check revolutionary prompt integration")
    
    print(f"\n💡 REVOLUTIONARY ACHIEVEMENTS:")
    if avg_confidence > 0.8:
        print(f"   🧠 High AI Confidence: {avg_confidence:.1%}")
    if avg_time < 60:
        print(f"   ⚡ Fast Performance: {avg_time:.2f}s average")
    if avg_features >= 2:
        print(f"   🚀 Revolutionary Features Active: {avg_features:.1f}/4 average")
    
    return results

if __name__ == "__main__":
    print("🔍 Checking server connection...")
    
    try:
        response = requests.get("http://localhost:8001/", timeout=5)
        if response.status_code == 200:
            print("✅ Revolutionary server is running!")
            test_revolutionary_dashboard()
        else:
            print("❌ Server not responding properly")
    except:
        print("❌ Cannot connect to server")
        print("💡 Make sure revolutionary server is running on port 8001")
