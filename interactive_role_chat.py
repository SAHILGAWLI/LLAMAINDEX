#!/usr/bin/env python3
"""
Interactive Role-Aware Chat Interface

This provides a command-line interface to test the role-aware chat system
with real-time interaction between citizen and officer roles.
"""

import requests
import json
import uuid
from typing import Dict, Any

class InteractiveRoleChat:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id = f"interactive_{uuid.uuid4().hex[:8]}"
        self.current_role = "citizen"
        self.last_response_id = None
        self.conversation_count = 0
        
    def send_message(self, message: str, instruction_type: str = None) -> Dict[str, Any]:
        """Send message with current role"""
        payload = {
            "session_id": self.session_id,
            "message": message,
            "speaker_role": self.current_role
        }
        
        if instruction_type:
            payload["officer_instruction_type"] = instruction_type
        if self.last_response_id and self.current_role == "officer":
            payload["original_response_id"] = self.last_response_id
            
        try:
            response = requests.post(
                f"{self.base_url}/citizen_chat",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                self.last_response_id = result['response_id']
                self.conversation_count += 1
                return result
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return None
    
    def display_response(self, response: Dict[str, Any]):
        """Display AI response"""
        if not response:
            return
            
        print("\n" + "="*60)
        print("🤖 AI RESPONSE")
        print("="*60)
        print(f"📄 {response['answer']}")
        print(f"\n📊 Confidence: {response['confidence_score']:.2f}")
        print(f"⚠️ Needs Review: {response['requires_officer_review']}")
        print(f"🆔 Response ID: {response['response_id']}")
        print("="*60)
        
    def switch_role(self):
        """Switch between citizen and officer roles"""
        if self.current_role == "citizen":
            self.current_role = "officer"
            print("\n🔄 Switched to OFFICER mode")
            print("You can now provide feedback, modifications, or approvals.")
        else:
            self.current_role = "citizen"
            print("\n🔄 Switched to CITIZEN mode")
            print("You can now ask legal questions.")
    
    def show_help(self):
        """Show available commands"""
        print("\n📋 AVAILABLE COMMANDS:")
        print("="*50)
        print("🔄 /switch    - Switch between citizen/officer roles")
        print("📊 /status    - Show current session status")
        print("❓ /help      - Show this help message")
        print("🚪 /quit      - Exit the chat")
        print("\n👮 OFFICER COMMANDS (when in officer mode):")
        print("📝 /modify    - Modify the last AI response")
        print("🔄 /regenerate - Regenerate the last AI response")
        print("✅ /approve   - Approve the last AI response")
        print("❌ /reject    - Reject the last AI response")
        print("="*50)
        
    def show_status(self):
        """Show current session status"""
        print(f"\n📊 SESSION STATUS:")
        print(f"🆔 Session ID: {self.session_id}")
        print(f"👤 Current Role: {self.current_role.upper()}")
        print(f"💬 Messages Sent: {self.conversation_count}")
        print(f"🔗 Last Response ID: {self.last_response_id}")
        
    def handle_officer_command(self, command: str, message: str):
        """Handle officer-specific commands"""
        instruction_map = {
            "/modify": "modify",
            "/regenerate": "regenerate", 
            "/approve": "approve",
            "/reject": "reject"
        }
        
        if command in instruction_map:
            if not self.last_response_id:
                print("❌ No previous response to modify. Send a citizen message first.")
                return
                
            instruction_type = instruction_map[command]
            print(f"\n👮 Officer {instruction_type}: {message}")
            
            response = self.send_message(message, instruction_type)
            self.display_response(response)
        else:
            print(f"❌ Unknown officer command: {command}")
    
    def run(self):
        """Main interactive loop"""
        print("🚀 INTERACTIVE ROLE-AWARE CHAT SYSTEM")
        print("="*60)
        print(f"Session ID: {self.session_id}")
        print(f"Current Role: {self.current_role.upper()}")
        print("\nType /help for available commands")
        print("="*60)
        
        while True:
            try:
                # Show current role in prompt
                role_icon = "👤" if self.current_role == "citizen" else "👮"
                user_input = input(f"\n{role_icon} {self.current_role.upper()}: ").strip()
                
                if not user_input:
                    continue
                    
                # Handle commands
                if user_input.startswith('/'):
                    command_parts = user_input.split(' ', 1)
                    command = command_parts[0].lower()
                    message = command_parts[1] if len(command_parts) > 1 else ""
                    
                    if command == '/quit':
                        print("👋 Goodbye!")
                        break
                    elif command == '/help':
                        self.show_help()
                    elif command == '/status':
                        self.show_status()
                    elif command == '/switch':
                        self.switch_role()
                    elif command in ['/modify', '/regenerate', '/approve', '/reject']:
                        if self.current_role != "officer":
                            print("❌ Officer commands only available in officer mode. Use /switch first.")
                        else:
                            if not message:
                                message = input(f"Enter {command[1:]} instruction: ").strip()
                            self.handle_officer_command(command, message)
                    else:
                        print(f"❌ Unknown command: {command}. Type /help for available commands.")
                        
                else:
                    # Regular message
                    print(f"\n📤 Sending {self.current_role} message...")
                    response = self.send_message(user_input)
                    self.display_response(response)
                    
                    # Show suggestions based on response
                    if response and response.get('requires_officer_review') and self.current_role == "citizen":
                        print("\n💡 TIP: This response is flagged for officer review.")
                        print("   Use /switch to become an officer and review/modify it.")
                        
            except KeyboardInterrupt:
                print("\n\n👋 Chat session ended.")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")

def main():
    """Main function"""
    # Check server connectivity
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code != 200:
            print("❌ Server not responding. Please start the server first.")
            return
    except:
        print("❌ Cannot connect to server. Please start the server first.")
        return
    
    # Start interactive chat
    chat = InteractiveRoleChat()
    chat.run()

if __name__ == "__main__":
    main()
