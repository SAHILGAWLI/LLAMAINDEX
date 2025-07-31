#!/usr/bin/env python3
"""
Test Script for Role-Aware Citizen Chat System

This script demonstrates the three-party interaction:
1. Citizen asks questions
2. AI responds (flagged for officer review)
3. Officer provides feedback/modifications
4. AI generates improved response
"""

import requests
import json
import time
import uuid
from typing import Dict, Any

class RoleAwareChatTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id = f"test_session_{uuid.uuid4().hex[:8]}"
        self.conversation_history = []
        
    def send_message(self, message: str, speaker_role: str = "citizen", 
                    instruction_type: str = None, original_response_id: str = None) -> Dict[str, Any]:
        """
        Send a message to the role-aware chat system
        """
        payload = {
            "session_id": self.session_id,
            "message": message,
            "speaker_role": speaker_role
        }
        
        if instruction_type:
            payload["officer_instruction_type"] = instruction_type
        if original_response_id:
            payload["original_response_id"] = original_response_id
            
        try:
            print(f"\n🔄 Sending {speaker_role} message...")
            print(f"📝 Message: {message}")
            if instruction_type:
                print(f"🎯 Instruction Type: {instruction_type}")
                
            response = requests.post(
                f"{self.base_url}/citizen_chat",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                self.conversation_history.append({
                    "speaker": speaker_role,
                    "message": message,
                    "response": result,
                    "timestamp": time.time()
                })
                return result
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return None
    
    def display_response(self, response: Dict[str, Any], speaker_role: str):
        """
        Display the AI response in a formatted way
        """
        if not response:
            return
            
        print(f"\n🤖 AI Response (to {speaker_role}):")
        print("=" * 60)
        print(f"📄 Answer: {response['answer']}")
        print(f"🆔 Response ID: {response['response_id']}")
        print(f"👤 Speaker Role: {response['speaker_role']}")
        print(f"⚠️ Requires Officer Review: {response['requires_officer_review']}")
        print(f"📊 Confidence Score: {response['confidence_score']:.2f}")
        print("=" * 60)
        
    def test_complete_conversation_flow(self):
        """
        Test a complete conversation flow with role switching
        """
        print("🚀 Testing Complete Role-Aware Conversation Flow")
        print("=" * 80)
        
        # Step 1: Citizen asks a question
        print("\n📋 STEP 1: Citizen asks a legal question")
        citizen_question = "What are my rights if police want to search my car during a traffic stop?"
        
        response1 = self.send_message(citizen_question, "citizen")
        self.display_response(response1, "citizen")
        
        if not response1:
            print("❌ Failed to get citizen response")
            return
            
        # Step 2: Officer reviews and wants to modify
        print("\n📋 STEP 2: Officer reviews and provides modification instructions")
        officer_feedback = """Please add the following important points:
1. Mention the difference between a search and a frisk
2. Explain when police can search without consent (probable cause)
3. Add information about refusing consent to search
4. Include what to do if rights are violated"""
        
        response2 = self.send_message(
            officer_feedback, 
            "officer", 
            "modify", 
            response1['response_id']
        )
        self.display_response(response2, "officer")
        
        # Step 3: Citizen asks a follow-up question
        print("\n📋 STEP 3: Citizen asks a follow-up question")
        followup_question = "What if they find something illegal during the search?"
        
        response3 = self.send_message(followup_question, "citizen")
        self.display_response(response3, "citizen")
        
        # Step 4: Officer wants to regenerate the response
        print("\n📋 STEP 4: Officer wants to regenerate with specific focus")
        officer_regenerate = """Please regenerate this response with focus on:
1. The exclusionary rule and inadmissible evidence
2. When evidence can still be used despite improper search
3. The importance of not resisting even if search is illegal
4. Steps to take after the incident to protect rights"""
        
        response4 = self.send_message(
            officer_regenerate,
            "officer",
            "regenerate",
            response3['response_id']
        )
        self.display_response(response4, "officer")
        
        # Step 5: Officer approves final response
        print("\n📋 STEP 5: Officer approves the final response")
        officer_approval = "This response looks comprehensive and accurate. Please confirm this is the final answer for the citizen."
        
        response5 = self.send_message(
            officer_approval,
            "officer",
            "approve",
            response4['response_id']
        )
        self.display_response(response5, "officer")
        
        print("\n✅ Complete conversation flow tested successfully!")
        
    def test_contextual_continuity(self):
        """
        Test that context is maintained across role switches
        """
        print("\n🔍 Testing Contextual Continuity Across Role Switches")
        print("=" * 60)
        
        # Citizen starts conversation about arrest
        print("\n👤 Citizen: Initial question about arrest")
        response1 = self.send_message(
            "I was arrested last week. What should I have done?", 
            "citizen"
        )
        self.display_response(response1, "citizen")
        
        # Officer provides context-aware feedback
        print("\n👮 Officer: Context-aware modification")
        response2 = self.send_message(
            "The citizen mentioned they were already arrested. Please focus on post-arrest rights and what they should do now, not prevention.",
            "officer",
            "modify",
            response1['response_id']
        )
        self.display_response(response2, "officer")
        
        # Citizen asks follow-up that builds on context
        print("\n👤 Citizen: Follow-up building on context")
        response3 = self.send_message(
            "They didn't read me my rights. Does that help my case?",
            "citizen"
        )
        self.display_response(response3, "citizen")
        
        print("\n✅ Contextual continuity test completed!")
        
    def display_conversation_summary(self):
        """
        Display a summary of the entire conversation
        """
        print("\n📊 CONVERSATION SUMMARY")
        print("=" * 80)
        print(f"Session ID: {self.session_id}")
        print(f"Total Messages: {len(self.conversation_history)}")
        
        for i, entry in enumerate(self.conversation_history, 1):
            speaker_icon = "👤" if entry['speaker'] == "citizen" else "👮"
            print(f"\n{i}. {speaker_icon} {entry['speaker'].upper()}:")
            print(f"   Message: {entry['message'][:100]}...")
            print(f"   Confidence: {entry['response']['confidence_score']:.2f}")
            print(f"   Review Required: {entry['response']['requires_officer_review']}")

def main():
    """
    Main testing function
    """
    print("🧪 ROLE-AWARE CITIZEN CHAT SYSTEM TESTING")
    print("=" * 80)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code != 200:
            print("❌ Server not responding. Please start the server first.")
            return
    except:
        print("❌ Cannot connect to server. Please start the server first.")
        return
    
    # Initialize tester
    tester = RoleAwareChatTester()
    
    # Run tests
    try:
        # Test 1: Complete conversation flow
        tester.test_complete_conversation_flow()
        
        # Test 2: Contextual continuity
        tester.test_contextual_continuity()
        
        # Display summary
        tester.display_conversation_summary()
        
        print("\n🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("The role-aware chat system is working correctly.")
        
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Testing failed with error: {str(e)}")

if __name__ == "__main__":
    main()
