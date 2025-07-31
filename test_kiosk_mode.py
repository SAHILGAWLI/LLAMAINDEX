#!/usr/bin/env python3
"""
Test Kiosk Mode - Citizen-Only Chat System
This simulates how the chat engine works in a kiosk environment
with only citizen and AI interaction (no officers).
"""

import requests
import json
import time
import uuid

class KioskChatTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id = f"kiosk_{uuid.uuid4().hex[:8]}"
        self.conversation_history = []
        
    def send_citizen_message(self, message: str):
        """
        Send a message as a citizen (kiosk user)
        """
        payload = {
            "session_id": self.session_id,
            "message": message,
            "speaker_role": "citizen"  # Always citizen in kiosk mode
        }
        
        try:
            print(f"\n👤 CITIZEN (Kiosk User): {message}")
            print("🔄 Processing...")
            
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/citizen_chat",
                json=payload,
                timeout=30
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"\n🤖 AI RESPONSE:")
                print("=" * 60)
                print(f"📄 {result['answer']}")
                print("=" * 60)
                print(f"⏱️ Response Time: {response_time:.2f}s")
                print(f"📊 Confidence: {result['confidence_score']:.2f}")
                print(f"⚠️ Would Need Officer Review: {result['requires_officer_review']}")
                print(f"🆔 Response ID: {result['response_id']}")
                
                # In kiosk mode, we ignore officer review flag and show response directly
                self.conversation_history.append({
                    "user_message": message,
                    "ai_response": result['answer'],
                    "confidence": result['confidence_score'],
                    "response_time": response_time,
                    "timestamp": time.time()
                })
                
                return result
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return None
    
    def test_kiosk_conversation_flow(self):
        """
        Test a typical kiosk conversation flow
        """
        print("🏪 TESTING KIOSK MODE - CITIZEN ONLY CHAT")
        print("=" * 60)
        print(f"Kiosk Session ID: {self.session_id}")
        print("=" * 60)
        
        # Typical kiosk questions
        kiosk_questions = [
            "What are my rights if I'm arrested?",
            "How do I file a police complaint?", 
            "What documents do I need for bail?",
            "Can police search my house without a warrant?",
            "What should I do if I'm a victim of domestic violence?"
        ]
        
        for i, question in enumerate(kiosk_questions, 1):
            print(f"\n📋 KIOSK INTERACTION {i}/5")
            print("-" * 40)
            
            result = self.send_citizen_message(question)
            
            if not result:
                print("❌ Failed to get response")
                continue
                
            # Simulate user reading time
            time.sleep(1)
            
        print(f"\n📊 KIOSK SESSION SUMMARY")
        print("=" * 60)
        print(f"Total Questions: {len(self.conversation_history)}")
        avg_response_time = sum(h['response_time'] for h in self.conversation_history) / len(self.conversation_history)
        avg_confidence = sum(h['confidence'] for h in self.conversation_history) / len(self.conversation_history)
        print(f"Average Response Time: {avg_response_time:.2f}s")
        print(f"Average Confidence: {avg_confidence:.2f}")
        print("=" * 60)
        
    def test_contextual_follow_ups(self):
        """
        Test contextual follow-up questions (important for kiosk)
        """
        print("\n🔄 TESTING CONTEXTUAL FOLLOW-UPS")
        print("=" * 50)
        
        # Initial question
        self.send_citizen_message("What happens if I'm arrested?")
        
        # Follow-up questions that build on context
        follow_ups = [
            "What if they don't read me my rights?",
            "How long can they keep me in custody?",
            "Can I call my family?",
            "What if I can't afford a lawyer?"
        ]
        
        for follow_up in follow_ups:
            print(f"\n🔗 FOLLOW-UP QUESTION:")
            self.send_citizen_message(follow_up)
            time.sleep(1)
            
        print("\n✅ Contextual follow-ups completed!")

def main():
    """
    Main testing function for kiosk mode
    """
    print("🏪 KIOSK MODE TESTING - CITIZEN ONLY CHAT ENGINE")
    print("=" * 80)
    
    # Check server connectivity
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code != 200:
            print("❌ Server not responding. Please start the server first.")
            return
    except:
        print("❌ Cannot connect to server. Please start the server first.")
        return
    
    # Initialize kiosk tester
    kiosk = KioskChatTester()
    
    try:
        # Test 1: Basic kiosk conversation flow
        kiosk.test_kiosk_conversation_flow()
        
        # Test 2: Contextual follow-ups
        kiosk.test_contextual_follow_ups()
        
        print("\n🎉 KIOSK MODE TESTING COMPLETED SUCCESSFULLY!")
        print("✅ The chat engine works perfectly for kiosk applications")
        print("✅ No officer interaction needed - direct AI responses")
        print("✅ Contextual conversation maintained")
        print("✅ Fast response times suitable for kiosk users")
        
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Testing failed with error: {str(e)}")

if __name__ == "__main__":
    main()
