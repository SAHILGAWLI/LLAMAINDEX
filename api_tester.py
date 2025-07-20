import streamlit as st
import requests
import uuid

st.title("LlamaIndex Pinecone Query API Tester")

api_url = st.text_input("API Base URL", value="http://localhost:8000")

st.header("Single-turn Query (POST /query)")
query_question = st.text_input("Enter your question (single-turn):", key="single")
if st.button("Ask (Single-turn)"):
    try:
        resp = requests.post(f"{api_url}/query", json={"question": query_question})
        st.write("Response:", resp.json().get("answer", resp.text))
    except Exception as e:
        st.error(f"Error: {e}")

st.header("Multi-turn Chat (POST /chat)")
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

def add_to_history(role, text):
    st.session_state["chat_history"].append({"role": role, "text": text})

# Display chat history
for msg in st.session_state["chat_history"]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['text']}")
    else:
        st.markdown(f"**Bot:** {msg['text']}")

chat_question = st.text_input("Your message (multi-turn):", key="multi")
if st.button("Send (Multi-turn)"):
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

if st.button("Reset Chat Session"):
    st.session_state["session_id"] = str(uuid.uuid4())
    st.session_state["chat_history"] = []
    st.success("Chat session reset!")
