#!/usr/bin/env python3
"""
Check existing Pinecone index status before adding new documents
"""

import os
from dotenv import load_dotenv
from pinecone import Pinecone
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore

# Load environment variables
load_dotenv()

def check_existing_index():
    """
    Check the current status of the zhoop index
    """
    print("🔍 Checking existing 'zhoop' index status...")
    print("=" * 50)
    
    # Setup Pinecone connection
    api_key = os.environ.get("PINECONE_API_KEY")
    if not api_key:
        print("❌ PINECONE_API_KEY not found in environment variables")
        return
    
    try:
        pc = Pinecone(api_key=api_key)
        pinecone_index = pc.Index("zhoop")
        
        # Get index statistics
        stats = pinecone_index.describe_index_stats()
        
        print("📊 Index Statistics:")
        print(f"   📈 Total vectors: {stats.get('total_vector_count', 0)}")
        print(f"   📏 Dimension: {stats.get('dimension', 'Unknown')}")
        print(f"   🏷️  Namespaces: {len(stats.get('namespaces', {}))}")
        
        if stats.get('namespaces'):
            print("\n🏷️  Namespace Details:")
            for namespace, ns_stats in stats.get('namespaces', {}).items():
                ns_name = namespace if namespace else "default"
                vector_count = ns_stats.get('vector_count', 0)
                print(f"   • {ns_name}: {vector_count} vectors")
        
        # Test query to see what's currently indexed
        print("\n🧪 Testing current knowledge base...")
        try:
            vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
            index = VectorStoreIndex.from_vector_store(vector_store)
            query_engine = index.as_query_engine(similarity_top_k=2)
            
            test_queries = [
                "What is BNS?",
                "Police procedures",
                "FIR guidelines"
            ]
            
            for query in test_queries:
                print(f"\n🔍 Query: '{query}'")
                try:
                    response = query_engine.query(query)
                    response_text = str(response)[:150] + "..." if len(str(response)) > 150 else str(response)
                    print(f"📝 Response: {response_text}")
                except Exception as e:
                    print(f"❌ Query failed: {e}")
                    
        except Exception as e:
            print(f"❌ Could not test queries: {e}")
        
        print(f"\n✅ Index 'zhoop' is ready to receive new documents!")
        print("🚀 You can now run 'python load_new_kd.py' to add NEW_KD documents")
        
    except Exception as e:
        print(f"❌ Error accessing index 'zhoop': {e}")
        print("Make sure:")
        print("   1. PINECONE_API_KEY is correctly set")
        print("   2. The 'zhoop' index exists in your Pinecone account")
        print("   3. You have proper access permissions")

if __name__ == "__main__":
    check_existing_index()
