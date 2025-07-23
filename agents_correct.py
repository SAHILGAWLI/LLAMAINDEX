# ---------------------------------------------
# CORRECT ReAct Agents Implementation
# Following Official LlamaIndex Documentation
# ---------------------------------------------
import os
import asyncio
import time
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# LlamaIndex imports (EXACTLY as in documentation)
from llama_index.core.agent.workflow import ReActAgent
from llama_index.core.workflow import Context
from llama_index.core.tools import QueryEngineTool
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

# ---------------------------------------------
# Setup (EXACTLY as in documentation)
# ---------------------------------------------
load_dotenv()

# Pinecone setup
api_key = os.environ["PINECONE_API_KEY"]
pc = Pinecone(api_key=api_key)
pinecone_index = pc.Index("zhoop")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
index = VectorStoreIndex.from_vector_store(vector_store)

# LLM setup (EXACTLY as in documentation)
llm = OpenAI(model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

# ---------------------------------------------
# Create Query Engines (SIMPLE)
# ---------------------------------------------
compliance_engine = index.as_query_engine(
    similarity_top_k=5,
    response_mode="tree_summarize"
)

laws_engine = index.as_query_engine(
    similarity_top_k=4,
    response_mode="compact"
)

# ---------------------------------------------
# Create Tools (EXACTLY as in documentation)
# ---------------------------------------------
query_engine_tools = [
    QueryEngineTool.from_defaults(
        query_engine=compliance_engine,
        name="compliance_checker",
        description=(
            "Analyzes legal compliance requirements for medical and legal cases. "
            "Use this to check BNS compliance, police procedural compliance, "
            "and generate actionable compliance checklists. "
            "Use a detailed plain text question as input to the tool."
        ),
    ),
    QueryEngineTool.from_defaults(
        query_engine=laws_engine,
        name="bns_laws",
        description=(
            "Provides information about BNS (Bharatiya Nyaya Sanhita) laws, "
            "sections, penalties, and legal provisions. Use this to find "
            "relevant law sections for specific legal situations. "
            "Use a detailed plain text question as input to the tool."
        ),
    ),
]

# ---------------------------------------------
# Create ReAct Agent (EXACTLY as in documentation)
# ---------------------------------------------
agent = ReActAgent(
    tools=query_engine_tools,
    llm=llm,
    # Optional system prompt for legal specialization
    system_prompt=(
        "You are a Legal Analysis AI specialized in Indian law. "
        "You have access to BNS (Bharatiya Nyaya Sanhita) legal framework "
        "and police procedural documents. Always provide structured, "
        "actionable legal analysis with specific law sections and compliance requirements."
    )
)

# Context to hold session/state (EXACTLY as in documentation)
ctx = Context(agent)

# ---------------------------------------------
# Simple Execution Functions (FOLLOWING OFFICIAL PATTERN)
# ---------------------------------------------
# Old individual functions removed - now using enhanced combined approach with timeout protection

async def run_agent_with_timeout(query: str, timeout: int = 45) -> str:
    """
    Run agent with timeout protection to prevent infinite loops
    """
    try:
        # EXACT pattern from documentation with timeout
        handler = agent.run(query, ctx=ctx)
        response = await asyncio.wait_for(handler, timeout=timeout)
        return str(response)
    except asyncio.TimeoutError:
        return f"⚠️ Agent timeout after {timeout}s - Analysis incomplete but system stable"
    except Exception as e:
        return f"❌ Agent error: {str(e)}"

async def run_combined_analysis(case_context: str) -> Dict[str, Any]:
    """
    Run both compliance and laws analysis in parallel with timeout protection
    """
    print(f"🚀 Starting ENHANCED combined legal analysis...")
    start_time = time.time()
    
    # Enhanced queries with timeout protection
    compliance_query = (
        f"Create a detailed legal compliance checklist for this medical malpractice case: {case_context}. "
        f"\n\nProvide EXACTLY 8-10 specific compliance items in this format:\n"
        f"1. [ITEM NAME] - Status: [Complete/Incomplete/Pending] - Priority: [High/Medium/Low] - Details: [Brief description]\n"
        f"\n\nFocus on:\n"
        f"- BNS legal compliance requirements\n"
        f"- Police investigation procedures\n"
        f"- Medical evidence documentation\n"
        f"- Hospital protocol compliance\n"
        f"- Patient rights and safety standards\n"
        f"\n\nEnd with: COMPLIANCE SCORE: X/10 items complete"
    )
    
    laws_query = (
        f"Analyze this medical malpractice case and find 5-7 most relevant BNS law sections: {case_context}. "
        f"\n\nFor each section, provide EXACTLY this format:\n"
        f"**Section XXX: [Title]**\n"
        f"- Description: [What this section covers]\n"
        f"- Severity: [High/Medium/Low] (High=imprisonment >7 years, Medium=1-7 years, Low=fines/<1 year)\n"
        f"- Relevance Score: X.X/1.0\n"
        f"- Application: [How it applies to this case]\n"
        f"- Potential Penalty: [Specific punishment]\n\n"
        f"Focus on sections related to:\n"
        f"- Medical negligence and malpractice\n"
        f"- Professional misconduct\n"
        f"- Endangering life through negligence\n"
        f"- Breach of duty of care\n"
        f"\n\nEnd with: LEGAL RISK ASSESSMENT: [High/Medium/Low] based on applicable sections"
    )
    
    # Run both analyses in parallel with timeout protection
    print(f"🏛️ Starting compliance analysis with 45s timeout...")
    print(f"⚖️ Starting laws analysis with 45s timeout...")
    
    compliance_task = asyncio.create_task(run_agent_with_timeout(compliance_query, 45))
    laws_task = asyncio.create_task(run_agent_with_timeout(laws_query, 45))
    
    # Wait for both to complete
    compliance_result, laws_result = await asyncio.gather(
        compliance_task, 
        laws_task,
        return_exceptions=True
    )
    
    total_time = time.time() - start_time
    
    # Handle any exceptions
    if isinstance(compliance_result, Exception):
        compliance_result = f"Compliance analysis failed: {str(compliance_result)}"
    
    if isinstance(laws_result, Exception):
        laws_result = f"Laws analysis failed: {str(laws_result)}"
    
    # Calculate success metrics
    compliance_success = not ("timeout" in str(compliance_result).lower() or "error" in str(compliance_result).lower())
    laws_success = not ("timeout" in str(laws_result).lower() or "error" in str(laws_result).lower())
    overall_success = compliance_success and laws_success
    
    print(f"✅ Enhanced analysis completed in {total_time:.2f}s")
    print(f"📊 Success rate: Compliance={compliance_success}, Laws={laws_success}, Overall={overall_success}")
    
    return {
        "compliance_analysis": compliance_result,
        "laws_analysis": laws_result,
        "generation_time": total_time,
        "success": overall_success,
        "compliance_success": compliance_success,
        "laws_success": laws_success,
        "timeout_protection": "enabled",
        "max_timeout_per_agent": "45 seconds"
    }

# ---------------------------------------------
# Test Function
# ---------------------------------------------
async def test_correct_implementation():
    """
    Test the correct implementation with a sample case
    """
    test_case = (
        "Medical malpractice case involving negligent surgery leading to patient complications. "
        "Hospital failed to follow proper protocols during emergency surgery."
    )
    
    print("🧪 Testing CORRECT ReAct Agent Implementation")
    print("=" * 60)
    
    try:
        # Test combined analysis
        result = await run_combined_analysis(test_case)
        
        print("\n📋 COMPLIANCE ANALYSIS:")
        print("-" * 40)
        print(result["compliance_analysis"])
        
        print("\n⚖️ LAWS ANALYSIS:")
        print("-" * 40)
        print(result["laws_analysis"])
        
        print(f"\n⏱️ Total execution time: {result['generation_time']:.2f}s")
        
        return result
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return {"error": str(e), "success": False}

# ---------------------------------------------
# Main execution
# ---------------------------------------------
if __name__ == "__main__":
    # Run the test
    result = asyncio.run(test_correct_implementation())
    print("\n🎯 Test completed!")
