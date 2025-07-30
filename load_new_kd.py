#!/usr/bin/env python3
"""
Enhanced Knowledge Base Loader for NEW_KD2 PDFs
Loads PDF files directly into Pinecone vector database
"""

import logging
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from pinecone import Pinecone, ServerlessSpec
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# ---------------------------------------------
# Environment Setup
# ---------------------------------------------
if "PINECONE_API_KEY" not in os.environ:
    raise EnvironmentError("PINECONE_API_KEY environment variable is not set")
if "OPENAI_API_KEY" not in os.environ:
    raise EnvironmentError("OPENAI_API_KEY environment variable is not set")

api_key = os.environ["PINECONE_API_KEY"]
openai_api_key = os.environ["OPENAI_API_KEY"]

# ---------------------------------------------
# Configure LlamaIndex Settings
# ---------------------------------------------
Settings.llm = OpenAI(model="gpt-4o-mini", api_key=openai_api_key)
Settings.embed_model = OpenAIEmbedding(api_key=openai_api_key)

# ---------------------------------------------
# Pinecone Setup - Connect to Existing Index
# ---------------------------------------------
pc = Pinecone(api_key=api_key)

# Connect to your existing "zhoop" index
index_name = "zhoop"
try:
    pinecone_index = pc.Index(index_name)

    # Get index stats to verify connection
    stats = pinecone_index.describe_index_stats()
    total_vectors = stats.get('total_vector_count', 0)

    print(f"✅ Connected to existing Pinecone index: {index_name}")
    print(f"📊 Current vectors in index: {total_vectors}")
    print(f"🔄 Will ADD new documents to existing knowledge base")

except Exception as e:
    print(f"❌ Error connecting to existing index {index_name}: {e}")
    print("Make sure the 'zhoop' index exists in your Pinecone account")
    raise

# ---------------------------------------------
# Document Loading and Processing
# ---------------------------------------------
def load_new_knowledge_base():
    """
    Load PDF documents from NEW_KD2 folder into Pinecone
    """
    print("🚀 Starting NEW_KD2 knowledge base loading...")
    
    # Path to your NEW_KD2 folder
    new_kd_path = "./NEW_KD2"
    
    if not os.path.exists(new_kd_path):
        raise FileNotFoundError(f"NEW_KD2 folder not found at: {new_kd_path}")
    
    # List files in NEW_KD2
    files = os.listdir(new_kd_path)
    pdf_files = [f for f in files if f.endswith('.pdf')]
    
    print(f"📁 Found {len(pdf_files)} PDF files in NEW_KD2:")
    for pdf_file in pdf_files:
        print(f"   📄 {pdf_file}")
    
    if not pdf_files:
        raise ValueError("No PDF files found in NEW_KD2 folder")
    
    # Load documents using SimpleDirectoryReader
    print("📖 Loading PDF documents...")
    try:
        # SimpleDirectoryReader automatically handles PDF parsing
        documents = SimpleDirectoryReader(
            input_dir=new_kd_path,
            required_exts=[".pdf"],  # Only load PDF files
            recursive=False  # Don't search subdirectories
        ).load_data()
        
        print(f"✅ Successfully loaded {len(documents)} document chunks")
        
        # Add metadata to documents for better organization
        for i, doc in enumerate(documents):
            # Extract filename from document metadata
            filename = getattr(doc, 'metadata', {}).get('file_name', f'document_{i}')
            
            # Add enhanced metadata
            doc.metadata.update({
                'source': 'NEW_KD2',
                'document_type': 'legal_document',
                'file_name': filename,
                'load_timestamp': str(pd.Timestamp.now()),
                'content_category': categorize_document(filename)
            })
            
        return documents
        
    except Exception as e:
        print(f"❌ Error loading documents: {e}")
        raise

def categorize_document(filename):
    """
    Categorize documents based on filename for better organization
    """
    filename_lower = filename.lower()
    
    if 'bns' in filename_lower and 'mapping' not in filename_lower:
        return 'bharatiya_nyaya_sanhita'
    elif 'bnss' in filename_lower:
        return 'bharatiya_nagarik_suraksha_sanhita'
    elif 'bsa' in filename_lower:
        return 'bharatiya_sakshya_adhiniyam'
    elif 'mapping' in filename_lower:
        return 'legal_mapping'
    elif 'handbook' in filename_lower:
        return 'legal_handbook'
    else:
        return 'legal_document'

def add_documents_to_existing_index(documents):
    """
    Add new documents to existing Pinecone index (append mode)
    """
    print("🔄 Adding new documents to existing Pinecone index...")

    try:
        # Get current index stats before adding
        stats_before = pinecone_index.describe_index_stats()
        vectors_before = stats_before.get('total_vector_count', 0)

        # Configure text splitter for better chunking
        text_splitter = SentenceSplitter(
            chunk_size=1024,  # Optimal chunk size for legal documents
            chunk_overlap=200,  # Overlap to maintain context
            separator=" "
        )

        # Create vector store pointing to existing index
        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # Create index from existing vector store (this connects to existing data)
        existing_index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            storage_context=storage_context
        )

        # Add new documents to the existing index
        print(f"📝 Processing {len(documents)} new documents...")
        for i, doc in enumerate(documents):
            print(f"   📄 Processing: {doc.metadata.get('file_name', f'Document {i+1}')}...")

        # Insert new documents (this appends to existing index)
        existing_index.insert_nodes(
            text_splitter.get_nodes_from_documents(documents),
            show_progress=True
        )

        # Get stats after adding
        stats_after = pinecone_index.describe_index_stats()
        vectors_after = stats_after.get('total_vector_count', 0)
        new_vectors = vectors_after - vectors_before

        print(f"✅ Successfully added documents to existing index!")
        print(f"📊 Vectors before: {vectors_before}")
        print(f"📊 Vectors after: {vectors_after}")
        print(f"🆕 New vectors added: {new_vectors}")

        return existing_index

    except Exception as e:
        print(f"❌ Error adding documents to index: {e}")
        raise

def test_knowledge_base(index):
    """
    Test the loaded knowledge base with sample queries
    """
    print("🧪 Testing knowledge base with sample queries...")
    
    test_queries = [
        "What are the punishments under BNS?",
        "FIR procedures under BNSS",
        "Evidence collection guidelines",
        "Medical negligence sections",
        "Cyber crime provisions"
    ]
    
    query_engine = index.as_query_engine(similarity_top_k=3)
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        try:
            response = query_engine.query(query)
            print(f"📝 Response: {str(response)[:200]}...")
        except Exception as e:
            print(f"❌ Error: {e}")

# ---------------------------------------------
# Main Execution
# ---------------------------------------------
if __name__ == "__main__":
    try:
        # Import pandas for timestamp
        import pandas as pd
        
        print("🎯 NEW_KD2 Knowledge Base Loader")
        print("=" * 50)
        
        # Step 1: Load documents
        documents = load_new_knowledge_base()
        
        # Step 2: Add documents to existing index
        index = add_documents_to_existing_index(documents)
        
        # Step 3: Test knowledge base
        test_knowledge_base(index)
        
        print("\n🎉 Knowledge base enhancement completed successfully!")
        print("=" * 50)
        print("📊 Summary:")
        print(f"   📄 New documents added: {len(documents)}")
        print(f"   🗂️  Existing index: {index_name}")
        print(f"   🔗 Vector store: Pinecone")
        print("   ✅ Status: Enhanced and ready for queries")
        print("\n🚀 Your platform now has enhanced legal intelligence!")
        print("   📚 BNS 2023 - Complete criminal law")
        print("   📚 BNSS 2023 - New criminal procedure code")
        print("   📚 BSA 2023 - New evidence law")
        print("   📚 Legal mapping and handbooks")
        
    except Exception as e:
        print(f"\n❌ Knowledge base loading failed: {e}")
        sys.exit(1)
