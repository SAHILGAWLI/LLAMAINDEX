# ---------------------------------------------
# Setup and Imports
# ---------------------------------------------
import os
import sys
import logging
from dotenv import load_dotenv
import openai
import pinecone
from pinecone import Pinecone, ServerlessSpec
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import VectorStoreIndex

# ---------------------------------------------
# Environment Variables and Logging
# ---------------------------------------------
load_dotenv()  # Load .env file

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# ---------------------------------------------
# API Keys Setup
# ---------------------------------------------
api_key = os.environ["PINECONE_API_KEY"]
openai.api_key = os.environ["OPENAI_API_KEY"]

# ---------------------------------------------
# Pinecone and LlamaIndex Setup
# ---------------------------------------------
pc = Pinecone(api_key=api_key)

# Connect to existing Pinecone index
pinecone_index = pc.Index("quickstart")

# Wrap with LlamaIndex's PineconeVectorStore
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

# Create the LlamaIndex wrapper
index = VectorStoreIndex.from_vector_store(vector_store)

# ---------------------------------------------
# Query Example (Dynamic User Input)
# ---------------------------------------------
# Query Loop: True RAG with RetrieverQueryEngine and GPT-4o-mini
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer

# 1. Create the LLM
llm = OpenAI(model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

# 2. Create chat memory with a reasonable token limit (adjustable)
memory = ChatMemoryBuffer.from_defaults(token_limit=3900)

# 3. Define a custom context prompt
context_prompt = (
    "You are a chatbot, able to have normal interactions, as well as talk "
    "about documents stored in the Pinecone index.\n"
    "Here are the relevant documents for the context:\n"
    "{context_str}\n"
    "Instruction: Use the previous chat history, or the context above, to interact and help the user."
)

# 4. Create the chat engine in 'condense_plus_context' mode
chat_engine = index.as_chat_engine(
    chat_mode="condense_question",
    memory=memory,
    llm=llm,
    context_prompt=context_prompt,
    verbose=False,
)

print("Type 'exit' to quit.")
print("Type 'exit' to quit. Type '/stream' to enter streaming mode, '/normal' to return to normal mode.")
streaming_mode = False
while True:
    try:
        user_query = input("Enter your question: ")
        if user_query.strip().lower() == 'exit':
            print("Exiting. Goodbye!")
            break
        elif user_query.strip().lower() == '/stream':
            streaming_mode = True
            print("[Streaming mode enabled]")
            continue
        elif user_query.strip().lower() == '/normal':
            streaming_mode = False
            print("[Normal mode enabled]")
            continue
        if streaming_mode:
            response = chat_engine.stream_chat(user_query)
            print("[Streaming response]:", end=" ")
            for token in response.response_gen:
                print(token, end="", flush=True)
            print()
        else:
            response = chat_engine.chat(user_query)
            print(response)
    except KeyboardInterrupt:
        print("\nExiting. Goodbye!")
        break
