# ---------------------------------------------
# ReAct Agents Configuration for Legal Platform
# ---------------------------------------------
import os
import asyncio
from typing import Dict, List, Any
from llama_index.core.agent.workflow import ReActAgent
from llama_index.core.workflow import Context
from llama_index.core.tools import QueryEngineTool
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

# Import existing setup from query_api
from query_api import pc, pinecone_index, vector_store, index, llm

# ---------------------------------------------
# Agent Base Class
# ---------------------------------------------
class BaseAgent:
    def __init__(self, name: str, tools: List[QueryEngineTool], system_prompt: str = None):
        self.name = name
        self.agent = ReActAgent(
            tools=tools,
            llm=llm,
            system_prompt=system_prompt,
            verbose=True
        )
        self.context = Context(self.agent)
    
    async def run(self, query: str) -> str:
        """Execute agent with query and return response"""
        try:
            handler = self.agent.run(query, ctx=self.context)
            response = await handler
            return str(response)
        except Exception as e:
            return f"Agent error: {str(e)}"

# ---------------------------------------------
# Specialized Query Engines for Different Domains
# ---------------------------------------------
class LegalQueryEngines:
    def __init__(self):
        # Use existing index for now, later we'll create specialized indexes
        self.base_index = index
        
        # Create specialized query engines
        self.compliance_engine = self.base_index.as_query_engine(
            similarity_top_k=5,
            response_mode="tree_summarize"
        )
        
        self.laws_engine = self.base_index.as_query_engine(
            similarity_top_k=3,
            response_mode="compact"
        )
        
        self.documents_engine = self.base_index.as_query_engine(
            similarity_top_k=4,
            response_mode="simple_summarize"
        )
        
        self.cases_engine = self.base_index.as_query_engine(
            similarity_top_k=6,
            response_mode="tree_summarize"
        )

# ---------------------------------------------
# Grid 1: Compliance Agent
# ---------------------------------------------
class ComplianceAgent(BaseAgent):
    def __init__(self, query_engines: LegalQueryEngines):
        tools = [
            QueryEngineTool.from_defaults(
                query_engine=query_engines.compliance_engine,
                name="fhir_compliance_checker",
                description=(
                    "Analyzes FHIR compliance requirements and current status. "
                    "Use this to check compliance items, generate checklists, "
                    "and assess compliance gaps. Input should be specific compliance questions."
                )
            ),
            QueryEngineTool.from_defaults(
                query_engine=query_engines.base_index.as_query_engine(),
                name="compliance_standards_database",
                description=(
                    "Provides information about compliance standards, regulations, "
                    "and best practices. Use for understanding compliance requirements "
                    "and getting detailed compliance guidance."
                )
            )
        ]
        
        system_prompt = (
            "You are a FHIR Compliance Specialist AI. Your role is to:\n"
            "1. Analyze compliance requirements for medical and legal cases\n"
            "2. Generate detailed compliance checklists\n"
            "3. Assess current compliance status\n"
            "4. Provide actionable recommendations\n"
            "5. Calculate compliance percentages and progress\n\n"
            "Always provide structured, actionable compliance information. "
            "Focus on specific, measurable compliance items."
        )
        
        super().__init__("ComplianceAgent", tools, system_prompt)

# ---------------------------------------------
# Grid 2: Legal Laws Agent
# ---------------------------------------------
class LegalLawsAgent(BaseAgent):
    def __init__(self, query_engines: LegalQueryEngines):
        tools = [
            QueryEngineTool.from_defaults(
                query_engine=query_engines.laws_engine,
                name="bns_laws_database",
                description=(
                    "Provides information about BNS (Bharatiya Nyaya Sanhita) laws, "
                    "sections, penalties, and legal provisions. Use this to find "
                    "relevant law sections for specific legal situations."
                )
            ),
            QueryEngineTool.from_defaults(
                query_engine=query_engines.base_index.as_query_engine(),
                name="legal_precedents_database",
                description=(
                    "Provides information about legal precedents, case law, "
                    "and judicial interpretations. Use for understanding how "
                    "laws have been applied in similar cases."
                )
            )
        ]
        
        system_prompt = (
            "You are a Legal Research Specialist AI. Your role is to:\n"
            "1. Find relevant BNS law sections for given legal situations\n"
            "2. Classify law severity (High/Medium/Low) based on penalties\n"
            "3. Calculate relevance scores for laws based on case context\n"
            "4. Provide clear explanations of legal provisions\n"
            "5. Suggest related laws and cross-references\n\n"
            "Always classify severity as: High (imprisonment >7 years), "
            "Medium (imprisonment 1-7 years), Low (fines or <1 year imprisonment). "
            "Provide relevance scores from 0.0 to 1.0."
        )
        
        super().__init__("LegalLawsAgent", tools, system_prompt)

# ---------------------------------------------
# Grid 3: Document Analysis Agent
# ---------------------------------------------
class DocumentAgent(BaseAgent):
    def __init__(self, query_engines: LegalQueryEngines):
        tools = [
            QueryEngineTool.from_defaults(
                query_engine=query_engines.documents_engine,
                name="document_analyzer",
                description=(
                    "Analyzes legal and medical documents, extracts key information, "
                    "and classifies document types. Use this to understand document "
                    "content and importance for cases."
                )
            ),
            QueryEngineTool.from_defaults(
                query_engine=query_engines.base_index.as_query_engine(),
                name="document_classifier",
                description=(
                    "Classifies documents by type (medical_evidence, legal_document, "
                    "witness_statement, expert_report, compliance_report) and "
                    "determines priority levels."
                )
            )
        ]
        
        system_prompt = (
            "You are a Document Intelligence Specialist AI. Your role is to:\n"
            "1. Analyze and summarize legal and medical documents\n"
            "2. Classify documents by type and priority\n"
            "3. Extract key information and insights\n"
            "4. Identify missing or required documents\n"
            "5. Assess document relevance to cases\n\n"
            "Document types: medical_evidence, legal_document, witness_statement, "
            "expert_report, compliance_report. Priority levels: high, medium, low. "
            "Always provide clear, concise document summaries."
        )
        
        super().__init__("DocumentAgent", tools, system_prompt)

# ---------------------------------------------
# Grid 4: Case Analysis Agent
# ---------------------------------------------
class CaseAnalysisAgent(BaseAgent):
    def __init__(self, query_engines: LegalQueryEngines):
        tools = [
            QueryEngineTool.from_defaults(
                query_engine=query_engines.cases_engine,
                name="case_precedent_search",
                description=(
                    "Searches for similar past cases, legal precedents, and "
                    "case outcomes. Use this to find cases with similar facts, "
                    "legal issues, or circumstances."
                )
            ),
            QueryEngineTool.from_defaults(
                query_engine=query_engines.base_index.as_query_engine(),
                name="case_outcome_analyzer",
                description=(
                    "Analyzes case outcomes, success rates, and patterns. "
                    "Use this to understand how similar cases were resolved "
                    "and predict potential outcomes."
                )
            )
        ]
        
        system_prompt = (
            "You are a Case Analysis Specialist AI. Your role is to:\n"
            "1. Find similar past cases based on facts and legal issues\n"
            "2. Calculate similarity scores between cases (0.0 to 1.0)\n"
            "3. Analyze case outcomes and success patterns\n"
            "4. Provide strategic insights for case preparation\n"
            "5. Identify key precedents and their relevance\n\n"
            "Always provide similarity scores, case outcomes, and actionable insights. "
            "Focus on cases that can inform strategy for the current case."
        )
        
        super().__init__("CaseAnalysisAgent", tools, system_prompt)

# ---------------------------------------------
# Agent Manager - Orchestrates All Agents
# ---------------------------------------------
class AgentManager:
    def __init__(self):
        self.query_engines = LegalQueryEngines()
        
        # Initialize all agents
        self.compliance_agent = ComplianceAgent(self.query_engines)
        self.legal_agent = LegalLawsAgent(self.query_engines)
        self.document_agent = DocumentAgent(self.query_engines)
        self.case_agent = CaseAnalysisAgent(self.query_engines)
        
        self.agents = {
            "compliance": self.compliance_agent,
            "legal": self.legal_agent,
            "documents": self.document_agent,
            "cases": self.case_agent
        }
    
    async def run_single_agent(self, agent_name: str, query: str) -> str:
        """Run a single agent with a query"""
        if agent_name not in self.agents:
            raise ValueError(f"Unknown agent: {agent_name}")
        
        agent = self.agents[agent_name]
        return await agent.run(query)
    
    async def run_all_agents(self, queries: Dict[str, str]) -> Dict[str, str]:
        """Run all agents in parallel with different queries"""
        tasks = {}
        
        for agent_name, query in queries.items():
            if agent_name in self.agents:
                tasks[agent_name] = asyncio.create_task(
                    self.agents[agent_name].run(query)
                )
        
        # Wait for all tasks to complete
        results = {}
        for agent_name, task in tasks.items():
            try:
                results[agent_name] = await task
            except Exception as e:
                results[agent_name] = f"Error: {str(e)}"
        
        return results
    
    async def populate_dashboard(self, case_id: str, case_context: str) -> Dict[str, str]:
        """
        Populate dashboard by running all agents in parallel (legacy method)
        """
        queries = {
            "compliance": f"Generate a FHIR compliance checklist for case {case_id} with context: {case_context}. Include specific compliance items, their current status, and completion percentage.",
            "legal": f"Find relevant BNS law sections for case context: {case_context}. Classify each law by severity (High/Medium/Low) and provide relevance scores.",
            "documents": f"Analyze and prioritize documents for case {case_id} with context: {case_context}. Classify document types and determine priority levels.",
            "cases": f"Find similar past cases to case {case_id} with context: {case_context}. Calculate similarity scores and analyze outcomes."
        }
        
        return await self.run_all_agents(queries)
    
    async def populate_dashboard_hierarchical(self, case_id: str, case_context: str) -> Dict[str, str]:
        """
        Populate dashboard using hierarchical execution for optimal results.
        
        Execution Order:
        1. Laws Agent (Most Independent) - Establishes legal framework
        2. Compliance Agent - Uses legal context for targeted compliance
        3. Documents Agent - Uses legal + compliance context for prioritization
        4. Cases Agent - Uses all previous context for enhanced similarity matching
        
        Args:
            case_id: Unique case identifier
            case_context: Initial case description
            
        Returns:
            Dict with agent responses including enhanced context
        """
        results = {}
        
        try:
            # TIER 1: Laws Agent (Foundation - Most Independent)
            print(f"🏛️ [TIER 1] Running Laws Agent for case {case_id}...")
            laws_query = f"Find relevant BNS law sections for case context: {case_context}. Classify each law by severity (High/Medium/Low) and provide relevance scores."
            laws_response = await self.run_single_agent("legal", laws_query)
            results["legal"] = laws_response
            
            # Extract key legal insights for next tier
            legal_context = f"\n\nLEGAL FRAMEWORK IDENTIFIED:\n{laws_response[:500]}..."
            
            # TIER 2: Compliance Agent (Enhanced with Legal Context)
            print(f"⚖️ [TIER 2] Running Compliance Agent with legal context...")
            compliance_query = (
                f"Generate a FHIR compliance checklist for case {case_id} with context: {case_context}"
                f"{legal_context}"
                f"\n\nFocus on compliance requirements specific to the identified legal sections. "
                f"Map FHIR standards to relevant BNS provisions and prioritize by legal severity."
            )
            compliance_response = await self.run_single_agent("compliance", compliance_query)
            results["compliance"] = compliance_response
            
            # Extract compliance insights for next tier
            compliance_context = f"\n\nCOMPLIANCE REQUIREMENTS:\n{compliance_response[:400]}..."
            
            # TIER 3: Documents Agent (Enhanced with Legal + Compliance Context)
            print(f"📄 [TIER 3] Running Documents Agent with legal and compliance context...")
            documents_query = (
                f"Analyze and prioritize documents for case {case_id} with context: {case_context}"
                f"{legal_context}"
                f"{compliance_context}"
                f"\n\nPrioritize documents based on:\n"
                f"1. Relevance to identified legal sections\n"
                f"2. Compliance verification requirements\n"
                f"3. Evidence strength for legal arguments\n"
                f"Classify document types and determine priority levels accordingly."
            )
            documents_response = await self.run_single_agent("documents", documents_query)
            results["documents"] = documents_response
            
            # Extract document insights for final tier
            documents_context = f"\n\nDOCUMENT ANALYSIS:\n{documents_response[:400]}..."
            
            # TIER 4: Cases Agent (Most Enhanced - Uses All Previous Context)
            print(f"🔍 [TIER 4] Running Cases Agent with full contextual enhancement...")
            cases_query = (
                f"Find similar past cases to case {case_id} with context: {case_context}"
                f"{legal_context}"
                f"{compliance_context}"
                f"{documents_context}"
                f"\n\nFind cases that match:\n"
                f"1. Similar legal sections and severity levels\n"
                f"2. Comparable compliance challenges\n"
                f"3. Similar document patterns and evidence types\n"
                f"Calculate similarity scores considering legal, compliance, and documentary factors. "
                f"Analyze outcomes and provide strategic insights based on the comprehensive case profile."
            )
            cases_response = await self.run_single_agent("cases", cases_query)
            results["cases"] = cases_response
            
            print(f"✅ Hierarchical dashboard population completed for case {case_id}")
            return results
            
        except Exception as e:
            print(f"❌ Error in hierarchical execution: {e}")
            # Fallback to parallel execution if hierarchical fails
            print("🔄 Falling back to parallel execution...")
            return await self.populate_dashboard(case_id, case_context)

# ---------------------------------------------
# Global Agent Manager Instance
# ---------------------------------------------
agent_manager = AgentManager()
