#!/usr/bin/env python3
"""
Deployment script for Legal Platform ReAct Agent API
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def run_command(command, description=""):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}")
    print(f"   Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return None

def check_environment():
    """Check if required environment variables are set"""
    print("🔍 Checking environment variables...")
    
    required_vars = ["OPENAI_API_KEY", "PINECONE_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("   Please set them in your .env file or environment")
        return False
    
    print("✅ All required environment variables are set")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    
    # Check if requirements.txt exists
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found")
        return False
    
    # Install dependencies
    result = run_command("pip install -r requirements.txt", "Installing Python packages")
    return result is not None

def check_pinecone_connection():
    """Check if Pinecone connection is working"""
    print("🔌 Testing Pinecone connection...")
    
    test_script = """
import os
from pinecone import Pinecone

try:
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index = pc.Index("quickstart")
    stats = index.describe_index_stats()
    print(f"✅ Pinecone connected: {stats['total_vector_count']} vectors")
except Exception as e:
    print(f"❌ Pinecone connection failed: {e}")
    exit(1)
"""
    
    result = run_command(f'python -c "{test_script}"', "Testing Pinecone connection")
    return result is not None

def check_openai_connection():
    """Check if OpenAI connection is working"""
    print("🤖 Testing OpenAI connection...")
    
    test_script = """
import os
from openai import OpenAI

try:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=5
    )
    print("✅ OpenAI connected successfully")
except Exception as e:
    print(f"❌ OpenAI connection failed: {e}")
    exit(1)
"""
    
    result = run_command(f'python -c "{test_script}"', "Testing OpenAI connection")
    return result is not None

def test_agents():
    """Test if agents can be initialized"""
    print("🤖 Testing agent initialization...")
    
    test_script = """
try:
    from agents import agent_manager
    print(f"✅ Agents initialized: {list(agent_manager.agents.keys())}")
except Exception as e:
    print(f"❌ Agent initialization failed: {e}")
    exit(1)
"""
    
    result = run_command(f'python -c "{test_script}"', "Testing agent initialization")
    return result is not None

def start_server(port=8000, host="0.0.0.0"):
    """Start the FastAPI server"""
    print(f"🚀 Starting server on {host}:{port}...")
    
    command = f"uvicorn query_api:app --host {host} --port {port} --reload"
    print(f"   Command: {command}")
    print("   Press Ctrl+C to stop the server")
    
    try:
        subprocess.run(command, shell=True, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")

def run_tests():
    """Run the test suite"""
    print("🧪 Running tests...")
    
    # Test basic API endpoints
    test_script = """
import requests
import time

# Wait for server to start
time.sleep(2)

try:
    # Test health endpoint
    response = requests.get("http://localhost:8000/health")
    if response.status_code == 200:
        print("✅ Health endpoint working")
    else:
        print(f"❌ Health endpoint failed: {response.status_code}")
    
    # Test agent status
    response = requests.get("http://localhost:8000/agents/status")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Agent status: {data['total_agents']} agents ready")
    else:
        print(f"❌ Agent status failed: {response.status_code}")
        
except Exception as e:
    print(f"❌ API tests failed: {e}")
"""
    
    result = run_command(f'python -c "{test_script}"', "Running API tests")
    return result is not None

def main():
    """Main deployment function"""
    print("🏛️ Legal Platform ReAct Agent API Deployment")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("query_api.py").exists():
        print("❌ query_api.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Deployment steps
    steps = [
        ("Environment Check", check_environment),
        ("Install Dependencies", install_dependencies),
        ("Test Pinecone Connection", check_pinecone_connection),
        ("Test OpenAI Connection", check_openai_connection),
        ("Test Agent Initialization", test_agents),
    ]
    
    print("🔄 Running deployment checks...")
    
    for step_name, step_func in steps:
        print(f"\n📋 Step: {step_name}")
        if not step_func():
            print(f"❌ Deployment failed at step: {step_name}")
            sys.exit(1)
        time.sleep(1)
    
    print("\n✅ All deployment checks passed!")
    print("\n🎯 Deployment Options:")
    print("1. Start development server (localhost)")
    print("2. Start production server (0.0.0.0)")
    print("3. Run tests only")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            start_server(host="127.0.0.1")
            break
        elif choice == "2":
            port = input("Enter port (default 8000): ").strip() or "8000"
            start_server(port=int(port))
            break
        elif choice == "3":
            run_tests()
            break
        elif choice == "4":
            print("👋 Deployment script exited")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()
