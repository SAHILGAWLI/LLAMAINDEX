#!/usr/bin/env python3
"""
Comprehensive Stress Test for Revolutionary Legal Intelligence System
"""

import requests
import json
import time
import asyncio
import concurrent.futures
from datetime import datetime

class LegalIntelligenceStressTester:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.results = []
        
    def test_all_crime_types(self):
        """Test all major crime types for performance and accuracy"""
        print("🎯 TESTING ALL CRIME TYPES")
        print("=" * 80)
        
        crime_test_cases = [
            {
                "name": "🚫 Drug Crime (NDPS Act)",
                "case_id": "STRESS-DRUG-001",
                "case_context": "Accused was found selling illegal substances including charas, ganja, and heroin near a school. Police recovered 2 kg of narcotic drugs during raid operation.",
                "expected_time": 25,
                "crime_type": "drug_crime"
            },
            {
                "name": "👶 Child Protection (POCSO Act)",
                "case_id": "STRESS-CHILD-001", 
                "case_context": "Inappropriate sexual behavior and assault against a 10-year-old minor child by the accused teacher in school premises. Victim suffered trauma.",
                "expected_time": 30,
                "crime_type": "child_crime"
            },
            {
                "name": "💻 Cyber Crime (IT Act)",
                "case_id": "STRESS-CYBER-001",
                "case_context": "Online banking fraud through phishing website where accused stole credit card details and transferred Rs 5 lakhs from multiple victim accounts.",
                "expected_time": 25,
                "crime_type": "cyber_crime"
            },
            {
                "name": "🏠 Domestic Violence (DV Act)",
                "case_id": "STRESS-DV-001",
                "case_context": "Husband physically assaulted wife demanding additional dowry money. Victim suffered multiple injuries and was denied access to household resources.",
                "expected_time": 35,
                "crime_type": "domestic_violence"
            },
            {
                "name": "🔄 Medical Negligence (Complex)",
                "case_id": "STRESS-MED-001",
                "case_context": "Medical negligence during cardiac surgery where doctor failed to follow proper protocols, resulting in patient complications, additional surgeries, and permanent disability.",
                "expected_time": 45,
                "crime_type": "medical_negligence"
            },
            {
                "name": "💰 Financial Fraud (Economic Offense)",
                "case_id": "STRESS-FRAUD-001",
                "case_context": "Large-scale financial fraud involving fake investment scheme where accused cheated multiple investors of Rs 50 crores through fraudulent promises.",
                "expected_time": 30,
                "crime_type": "financial_fraud"
            },
            {
                "name": "🔫 Violent Crime (Assault)",
                "case_id": "STRESS-ASSAULT-001",
                "case_context": "Accused attacked victim with sharp weapon causing grievous injuries during property dispute. Victim hospitalized with life-threatening wounds.",
                "expected_time": 25,
                "crime_type": "violent_crime"
            },
            {
                "name": "🚗 Traffic Crime (Motor Vehicle)",
                "case_id": "STRESS-TRAFFIC-001",
                "case_context": "Rash and negligent driving causing death of pedestrian. Accused was driving under influence of alcohol and fled from accident scene.",
                "expected_time": 20,
                "crime_type": "traffic_crime"
            },
            {
                "name": "🏛️ Corruption (Prevention of Corruption Act)",
                "case_id": "STRESS-CORRUPT-001",
                "case_context": "Government official demanded and accepted bribe of Rs 2 lakhs for approving construction permit. Transaction recorded through sting operation.",
                "expected_time": 35,
                "crime_type": "corruption"
            },
            {
                "name": "🔥 Arson (Property Crime)",
                "case_id": "STRESS-ARSON-001",
                "case_context": "Accused intentionally set fire to commercial building causing property damage worth Rs 1 crore and endangering lives of occupants.",
                "expected_time": 25,
                "crime_type": "property_crime"
            }
        ]
        
        for i, test_case in enumerate(crime_test_cases, 1):
            print(f"\n{'='*20} CRIME TEST {i}/{len(crime_test_cases)} {'='*20}")
            print(f"🧪 {test_case['name']}")
            print(f"⏱️ Expected Time: <{test_case['expected_time']}s")
            print(f"🎯 Crime Type: {test_case['crime_type']}")
            print("=" * 80)
            
            result = self.run_single_test(test_case)
            self.results.append(result)
            
            # Brief pause between tests
            time.sleep(2)
        
        return self.results
    
    def test_edge_cases(self):
        """Test edge cases and unusual scenarios"""
        print("\n🔍 TESTING EDGE CASES")
        print("=" * 80)
        
        edge_cases = [
            {
                "name": "📝 Very Long Case Description",
                "case_id": "EDGE-LONG-001",
                "case_context": "This is an extremely detailed case involving multiple accused persons, numerous witnesses, complex evidence chain, multiple crime scenes across different jurisdictions, involving various sections of BNS, BNSS, BSA, NDPS Act, POCSO Act, IT Act, and other specialized legislation. " * 5,
                "expected_time": 60,
                "crime_type": "complex_multi_crime"
            },
            {
                "name": "🔤 Very Short Case Description", 
                "case_id": "EDGE-SHORT-001",
                "case_context": "Theft case.",
                "expected_time": 15,
                "crime_type": "simple_crime"
            },
            {
                "name": "🌐 Multi-Jurisdictional Case",
                "case_id": "EDGE-MULTI-001",
                "case_context": "International cybercrime involving multiple countries, cross-border financial transactions, cryptocurrency fraud, involving Indian IT Act, international treaties, and coordination with foreign law enforcement agencies.",
                "expected_time": 50,
                "crime_type": "international_crime"
            },
            {
                "name": "⚖️ Multiple Crime Types",
                "case_id": "EDGE-COMBO-001",
                "case_context": "Case involving drug trafficking, child exploitation, cybercrime, money laundering, and corruption - all interconnected in a single criminal enterprise with multiple accused and victims.",
                "expected_time": 55,
                "crime_type": "multi_crime_complex"
            },
            {
                "name": "🔍 Ambiguous Case Type",
                "case_id": "EDGE-AMBIG-001",
                "case_context": "Incident occurred involving some persons and some activities that may or may not constitute criminal behavior under applicable laws and regulations.",
                "expected_time": 40,
                "crime_type": "ambiguous_case"
            }
        ]
        
        for i, test_case in enumerate(edge_cases, 1):
            print(f"\n{'='*15} EDGE CASE {i}/{len(edge_cases)} {'='*15}")
            print(f"🧪 {test_case['name']}")
            print(f"⏱️ Expected Time: <{test_case['expected_time']}s")
            print("=" * 80)
            
            result = self.run_single_test(test_case)
            self.results.append(result)
            
            time.sleep(2)
    
    def test_concurrent_load(self):
        """Test system under concurrent load"""
        print("\n🚀 TESTING CONCURRENT LOAD")
        print("=" * 80)
        
        concurrent_cases = [
            {
                "case_id": f"LOAD-{i:03d}",
                "case_context": f"Drug crime case {i} involving illegal substance distribution and trafficking operations."
            }
            for i in range(1, 6)  # 5 concurrent requests
        ]
        
        print(f"🔄 Running {len(concurrent_cases)} concurrent requests...")
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(self.run_api_request, case)
                for case in concurrent_cases
            ]
            
            concurrent_results = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    concurrent_results.append(result)
                except Exception as e:
                    print(f"❌ Concurrent request failed: {e}")
                    concurrent_results.append({"success": False, "error": str(e)})
        
        total_time = time.time() - start_time
        successful_requests = sum(1 for r in concurrent_results if r.get("success", False))
        
        print(f"📊 Concurrent Load Results:")
        print(f"   Total Time: {total_time:.2f}s")
        print(f"   Successful Requests: {successful_requests}/{len(concurrent_cases)}")
        print(f"   Success Rate: {(successful_requests/len(concurrent_cases))*100:.1f}%")
        print(f"   Average Time per Request: {total_time/len(concurrent_cases):.2f}s")
        
        return concurrent_results
    
    def run_single_test(self, test_case):
        """Run a single test case"""
        try:
            start_time = time.time()
            
            response = requests.post(
                f"{self.base_url}/dashboard/populate-optimized",
                json={
                    "case_id": test_case["case_id"],
                    "case_context": test_case["case_context"]
                },
                timeout=300
            )
            
            end_time = time.time()
            actual_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Performance analysis
                expected_time = test_case["expected_time"]
                performance_ratio = actual_time / expected_time
                
                if actual_time <= expected_time:
                    performance_status = "🚀 EXCELLENT"
                elif actual_time <= expected_time * 1.5:
                    performance_status = "✅ GOOD"
                elif actual_time <= expected_time * 2:
                    performance_status = "⚠️ ACCEPTABLE"
                else:
                    performance_status = "❌ SLOW"
                
                # Check for errors
                legal_compliance = data.get('legal_compliance', '')
                bns_laws = data.get('bns_laws', '')
                has_errors = "Enhanced agent analysis failed" in legal_compliance or "Enhanced agent analysis failed" in bns_laws
                
                # Success metrics
                success_metrics = data.get('success_metrics', {})
                overall_success = success_metrics.get('overall', False)
                ai_confidence = data.get('ai_confidence', 0)
                
                print(f"✅ Response: {actual_time:.2f}s | {performance_status}")
                print(f"   Expected: {expected_time}s | Actual: {actual_time:.2f}s | Ratio: {performance_ratio:.2f}x")
                print(f"   Success: {'✅' if overall_success else '❌'} | AI Confidence: {ai_confidence:.1%}")
                print(f"   Errors: {'❌ Yes' if has_errors else '✅ None'}")
                
                return {
                    "test_name": test_case["name"],
                    "case_id": test_case["case_id"],
                    "crime_type": test_case.get("crime_type", "unknown"),
                    "expected_time": expected_time,
                    "actual_time": actual_time,
                    "performance_ratio": performance_ratio,
                    "performance_status": performance_status,
                    "overall_success": overall_success,
                    "ai_confidence": ai_confidence,
                    "has_errors": has_errors,
                    "success": True
                }
            else:
                print(f"❌ HTTP Error {response.status_code}")
                return {
                    "test_name": test_case["name"],
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return {
                "test_name": test_case["name"],
                "success": False,
                "error": str(e)
            }
    
    def run_api_request(self, case_data):
        """Helper method for concurrent testing"""
        try:
            response = requests.post(
                f"{self.base_url}/dashboard/populate-optimized",
                json=case_data,
                timeout=120
            )
            return {
                "case_id": case_data["case_id"],
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds()
            }
        except Exception as e:
            return {
                "case_id": case_data["case_id"],
                "success": False,
                "error": str(e)
            }
    
    def generate_final_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*100)
        print("📊 COMPREHENSIVE STRESS TEST REPORT")
        print("="*100)
        
        successful_tests = [r for r in self.results if r.get("success", False)]
        failed_tests = [r for r in self.results if not r.get("success", False)]
        
        if successful_tests:
            avg_time = sum(r["actual_time"] for r in successful_tests) / len(successful_tests)
            avg_confidence = sum(r["ai_confidence"] for r in successful_tests) / len(successful_tests)
            avg_performance_ratio = sum(r["performance_ratio"] for r in successful_tests) / len(successful_tests)
            
            excellent_count = sum(1 for r in successful_tests if "EXCELLENT" in r["performance_status"])
            good_count = sum(1 for r in successful_tests if "GOOD" in r["performance_status"])
            acceptable_count = sum(1 for r in successful_tests if "ACCEPTABLE" in r["performance_status"])
            slow_count = sum(1 for r in successful_tests if "SLOW" in r["performance_status"])
            
            error_count = sum(1 for r in successful_tests if r.get("has_errors", False))
            
            print(f"📈 PERFORMANCE SUMMARY:")
            print(f"   Total Tests: {len(self.results)}")
            print(f"   Successful: {len(successful_tests)}")
            print(f"   Failed: {len(failed_tests)}")
            print(f"   Success Rate: {(len(successful_tests)/len(self.results))*100:.1f}%")
            
            print(f"\n⏱️ TIMING ANALYSIS:")
            print(f"   Average Response Time: {avg_time:.2f}s")
            print(f"   Average Performance Ratio: {avg_performance_ratio:.2f}x")
            print(f"   🚀 Excellent: {excellent_count}")
            print(f"   ✅ Good: {good_count}")
            print(f"   ⚠️ Acceptable: {acceptable_count}")
            print(f"   ❌ Slow: {slow_count}")
            
            print(f"\n🧠 QUALITY METRICS:")
            print(f"   Average AI Confidence: {avg_confidence:.1%}")
            print(f"   Tests with Errors: {error_count}/{len(successful_tests)}")
            print(f"   Error Rate: {(error_count/len(successful_tests))*100:.1f}%")
            
            # Crime type performance
            crime_performance = {}
            for result in successful_tests:
                crime_type = result.get("crime_type", "unknown")
                if crime_type not in crime_performance:
                    crime_performance[crime_type] = []
                crime_performance[crime_type].append(result["actual_time"])
            
            print(f"\n🎯 CRIME TYPE PERFORMANCE:")
            for crime_type, times in crime_performance.items():
                avg_time_for_crime = sum(times) / len(times)
                print(f"   {crime_type}: {avg_time_for_crime:.2f}s avg ({len(times)} tests)")
        
        if failed_tests:
            print(f"\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"   {test['test_name']}: {test.get('error', 'Unknown error')}")
        
        # Overall assessment
        if len(successful_tests) / len(self.results) >= 0.9:
            print(f"\n🎉 OVERALL ASSESSMENT: EXCELLENT")
            print(f"✅ System is production-ready with outstanding performance!")
        elif len(successful_tests) / len(self.results) >= 0.8:
            print(f"\n✅ OVERALL ASSESSMENT: GOOD")
            print(f"✅ System is reliable with good performance!")
        elif len(successful_tests) / len(self.results) >= 0.7:
            print(f"\n⚠️ OVERALL ASSESSMENT: ACCEPTABLE")
            print(f"⚠️ System works but needs some optimization!")
        else:
            print(f"\n❌ OVERALL ASSESSMENT: NEEDS WORK")
            print(f"❌ System requires significant improvements!")

def main():
    print("🚀 REVOLUTIONARY LEGAL INTELLIGENCE STRESS TEST")
    print("=" * 100)
    print(f"🕐 Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check server connection
    try:
        response = requests.get("http://localhost:8001/", timeout=5)
        if response.status_code != 200:
            print("❌ Server not responding properly")
            return
    except:
        print("❌ Cannot connect to server on port 8001")
        print("💡 Make sure the revolutionary server is running!")
        return
    
    print("✅ Server connection confirmed!")
    
    # Initialize tester
    tester = LegalIntelligenceStressTester()
    
    # Run comprehensive tests
    print("\n🎯 Starting comprehensive stress testing...")
    
    # Test all crime types
    tester.test_all_crime_types()
    
    # Test edge cases
    tester.test_edge_cases()
    
    # Test concurrent load
    tester.test_concurrent_load()
    
    # Generate final report
    tester.generate_final_report()
    
    print(f"\n🕐 Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎉 Comprehensive stress testing complete!")

if __name__ == "__main__":
    main()
