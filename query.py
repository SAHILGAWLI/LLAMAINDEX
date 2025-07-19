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
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever

# 1. Create the retriever from your index
retriever = VectorIndexRetriever(index=index)

# 2. Create the LLM
llm = OpenAI(model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

# 3. Create the RAG Query Engine
query_engine = RetrieverQueryEngine.from_args(retriever, llm=llm)

# 4. Interactive query loop
print("Type 'exit' to quit.")
while True:
    try:
        user_query = input("Enter your question: ")
        if user_query.strip().lower() == 'exit':
            print("Exiting. Goodbye!")
            break
        response = query_engine.query(user_query)
        print(response)
    except KeyboardInterrupt:
        print("\nExiting. Goodbye!")
        break
