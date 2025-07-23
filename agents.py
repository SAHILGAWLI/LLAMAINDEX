# ---------------------------------------------
# ReAct Agents Configuration for Legal Platform
# ---------------------------------------------
import os
import asyncio
import time
from typing import Dict, List, Any, Optional
from llama_index.core.agent.workflow import ReActAgent
from llama_index.core.workflow import Context
from llama_index.core.tools import QueryEngineTool
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler
import logging
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
        # Add a callback manager to trace agent execution
        self.llama_debug_handler = LlamaDebugHandler()
        self.callback_manager = CallbackManager([self.llama_debug_handler])
        
        self.agent = ReActAgent(
            tools=tools,
            llm=llm,
            system_prompt=system_prompt,
            callback_manager=self.callback_manager,
            max_iterations=50,  # Set a higher but safe limit
            verbose=True
        )
        self.context = Context(self.agent)
    
    async def run(self, query: str) -> str:
        """Execute agent with query and return response"""
        print(f"\n[AGENT RUN] Starting agent: {self.name} with query: '{query[:100]}...'\n")
        try:
            # Use the correct method for ReActAgent workflow execution
            handler = self.agent.run(query, ctx=self.context)
            response = await handler
            print(f"✅ Agent {self.name} completed successfully")
            return str(response)
        except Exception as e:
            logging.error(f"Agent '{self.name}' failed with error: {e}")
            # Log the trace for debugging
            print(f"--- Agent Trace for {self.name} ---")
            try:
                if hasattr(self.llama_debug_handler, 'get_events'):
                    events = self.llama_debug_handler.get_events()
                    for event in events[-5:]:  # Show last 5 events
                        print(f"  {event}")
            except:
                print("  Unable to retrieve trace events")
            print("--- End Trace ---")
            return f"Agent error: {str(e)}"
        finally:
            # Optional: print trace even on success for debugging
            # print(f"--- Agent Trace for {self.name} ---")
            # if hasattr(self.llama_debug_handler, 'get_events'):
            #     events = self.llama_debug_handler.get_events()
            #     for event in events[-3:]:
            #         print(f"  {event}")
            # print("--- End Trace ---")
            pass

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
            tier1_start = time.time()
            laws_query = f"Find relevant BNS law sections for case context: {case_context}. Classify each law by severity (High/Medium/Low) and provide relevance scores."
            laws_response = await self.run_single_agent("legal", laws_query)
            results["legal"] = laws_response
            print(f"✅ TIER 1 completed in {time.time() - tier1_start:.2f}s")
            
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
# ---------------------------------------------
# Live Cases Agent - Grid 5 Integration
# ---------------------------------------------
class LiveCasesAgent(object):
    """
    Specialized agent for fetching and analyzing live legal cases
    from Indian Kanoon API with intelligent query construction
    """
    
    def __init__(self, query_engines: LegalQueryEngines):
        from indian_kanoon_client import get_indian_kanoon_client
        from query_builder import get_query_builder
        
        self.ik_client = get_indian_kanoon_client()
        self.query_builder = get_query_builder()
        
        # Tools for live case analysis
        tools = [
            QueryEngineTool.from_defaults(
                query_engine=query_engines.base_index.as_query_engine(),
                name="legal_knowledge_base",
                description=(
                    "Access to comprehensive legal knowledge base including "
                    "BNS provisions, case law, and legal precedents. Use this "
                    "to understand legal context and validate case relevance."
                )
            ),
            QueryEngineTool.from_defaults(
                query_engine=query_engines.base_index.as_query_engine(),
                name="case_similarity_analyzer",
                description=(
                    "Analyzes similarity between cases based on legal facts, "
                    "circumstances, and legal issues. Use this to score "
                    "case relevance and identify key similarities."
                )
            )
        ]
        
        system_prompt = (
            "You are a Live Cases Analysis Specialist AI integrated with Indian Kanoon API. Your role is to:\n"
            "1. Fetch real legal cases from Indian courts using intelligent search queries\n"
            "2. Analyze case relevance and similarity to the current case\n"
            "3. Extract key legal insights, outcomes, and precedents\n"
            "4. Provide citation analysis and legal authority assessment\n"
            "5. Generate actionable insights for legal strategy\n\n"
            "You have access to 2.5+ million Indian court cases through Indian Kanoon API. "
            "Always prioritize Supreme Court and High Court cases for higher legal authority. "
            "Focus on cases with similar BNS sections, fact patterns, and legal issues. "
            "Provide similarity scores, case outcomes, and strategic recommendations."
        )
        
        # super().__init__ removed: not inheriting from ReActAgent. All initialization handled above.
    
    async def search_and_analyze_cases(self, case_context: str, laws_agent_output: str = "") -> Dict:
        """
        Search for relevant live cases and perform comprehensive analysis
        
        Args:
            case_context: Description of the current case
            laws_agent_output: Output from Laws Agent with BNS sections
            
        Returns:
            Dict containing live cases with analysis and metadata
        """
        try:
            # Build intelligent search strategy
            search_strategy = self.query_builder.build_comprehensive_search_strategy(
                case_context, laws_agent_output
            )
            
            # Perform primary search
            primary_results = await self.ik_client.search_cases(
                query=search_strategy['primary_search']['query'],
                doctypes=search_strategy['primary_search']['doctypes'],
                maxcases=search_strategy['primary_search']['max_cases']
            )
            
            live_cases = []
            api_calls_made = 1
            
            # Process primary results
            if primary_results.get('docs'):
                live_cases.extend(await self._process_search_results(
                    primary_results['docs'], case_context, laws_agent_output
                ))
                api_calls_made += len(primary_results['docs'][:5])  # Limit detailed analysis
            
            # Fallback search if insufficient results
            if len(live_cases) < 5 and search_strategy['fallback_search']['query']:
                fallback_results = await self.ik_client.search_cases(
                    query=search_strategy['fallback_search']['query'],
                    doctypes=search_strategy['fallback_search']['doctypes'],
                    maxcases=search_strategy['fallback_search']['max_cases']
                )
                
                if fallback_results.get('docs'):
                    fallback_cases = await self._process_search_results(
                        fallback_results['docs'], case_context, laws_agent_output
                    )
                    live_cases.extend(fallback_cases)
                    api_calls_made += len(fallback_results['docs'][:3])
            
            # Sort by similarity score and limit results
            live_cases.sort(key=lambda x: x.get('similarity_score', 0), reverse=True)
            live_cases = live_cases[:15]  # Top 15 most relevant cases
            
            # Perform citation analysis for top cases
            citation_data = await self._analyze_citations(live_cases[:5])
            api_calls_made += 5
            
            # Generate case analytics
            case_analytics = self._generate_case_analytics(live_cases)
            
            return {
                'live_cases': live_cases,
                'citation_network': citation_data,
                'case_analytics': case_analytics,
                'search_metadata': {
                    **search_strategy['search_metadata'],
                    'primary_query': search_strategy['primary_search']['query'],
                    'fallback_query': search_strategy['fallback_search']['query'],
                    'total_cases_found': len(live_cases),
                    'api_calls_made': api_calls_made
                }
            }
            
        except Exception as e:
            logging.error(f"Error in live cases search: {e}")
            return {
                'live_cases': [],
                'citation_network': None,
                'case_analytics': None,
                'search_metadata': {'error': str(e)}
            }
    
    async def _process_search_results(self, docs: List[Dict], case_context: str, 
                                    laws_context: str) -> List[Dict]:
        """Process search results and calculate similarity scores"""
        processed_cases = []
        
        for doc in docs[:10]:  # Limit processing to top 10 results
            try:
                # Calculate similarity score using AI
                similarity_score = await self._calculate_similarity_score(
                    doc, case_context, laws_context
                )
                
                # Extract BNS sections from case
                bns_sections = self._extract_bns_sections_from_case(doc)
                
                # Generate case summary
                summary = await self._generate_case_summary(doc, case_context)
                
                processed_case = {
                    'tid': doc.get('tid', 0),
                    'title': doc.get('title', 'Unknown Case'),
                    'court': self._extract_court_name(doc.get('docsource', '')),
                    'date': doc.get('date'),
                    'bns_sections': bns_sections,
                    'similarity_score': similarity_score,
                    'case_outcome': self._extract_case_outcome(doc),
                    'indian_kanoon_url': f"https://indiankanoon.org/doc/{doc.get('tid', 0)}/",
                    'summary': summary,
                    'headline': doc.get('headline', ''),
                    'docsource': doc.get('docsource', ''),
                    'docsize': doc.get('docsize', 0)
                }
                
                processed_cases.append(processed_case)
                
            except Exception as e:
                logging.warning(f"Error processing case {doc.get('tid', 'unknown')}: {e}")
                continue
        
        return processed_cases
    
    async def _calculate_similarity_score(self, doc: Dict, case_context: str, 
                                        laws_context: str) -> float:
        """Calculate AI-powered similarity score between cases"""
        try:
            # Use the case similarity analyzer tool
            similarity_query = (
                f"Calculate similarity score between current case context: '{case_context}' "
                f"and this legal case: Title: {doc.get('title', '')} "
                f"Headline: {doc.get('headline', '')} "
                f"Legal context: {laws_context} "
                f"Consider legal issues, fact patterns, BNS sections, and case circumstances. "
                f"Return a similarity score between 0.0 and 1.0."
            )
            
            response = await self.run_tool("case_similarity_analyzer", similarity_query)
            
            # Extract numerical score from response
            import re
            score_match = re.search(r'\b0\.[0-9]+\b|\b1\.0\b', response)
            if score_match:
                return float(score_match.group())
            
            # Fallback: basic keyword matching
            return self._basic_similarity_score(doc, case_context)
            
        except Exception as e:
            logging.warning(f"Error calculating similarity score: {e}")
            return self._basic_similarity_score(doc, case_context)
    
    def _basic_similarity_score(self, doc: Dict, case_context: str) -> float:
        """Basic similarity scoring based on keyword matching"""
        case_text = f"{doc.get('title', '')} {doc.get('headline', '')}".lower()
        context_words = set(case_context.lower().split())
        case_words = set(case_text.split())
        
        if not case_words:
            return 0.0
        
        common_words = context_words.intersection(case_words)
        return min(len(common_words) / len(context_words) * 2, 1.0)  # Scale up
    
    def _extract_bns_sections_from_case(self, doc: Dict) -> List[str]:
        """Extract BNS sections mentioned in the case"""
        text = f"{doc.get('title', '')} {doc.get('headline', '')}"
        return self.query_builder.extract_bns_sections(text)
    
    def _extract_court_name(self, docsource: str) -> str:
        """Extract readable court name from docsource"""
        court_mappings = {
            'supremecourt': 'Supreme Court of India',
            'delhi': 'Delhi High Court',
            'bombay': 'Bombay High Court',
            'kolkata': 'Calcutta High Court',
            'chennai': 'Madras High Court',
            'allahabad': 'Allahabad High Court'
        }
        
        for key, name in court_mappings.items():
            if key in docsource.lower():
                return name
        
        return docsource or 'Unknown Court'
    
    def _extract_case_outcome(self, doc: Dict) -> Optional[str]:
        """Extract case outcome from case text"""
        text = f"{doc.get('title', '')} {doc.get('headline', '')}".lower()
        
        if any(word in text for word in ['convicted', 'guilty', 'sentenced']):
            return 'Conviction'
        elif any(word in text for word in ['acquitted', 'discharged', 'not guilty']):
            return 'Acquittal'
        elif any(word in text for word in ['dismissed', 'rejected']):
            return 'Dismissed'
        elif any(word in text for word in ['allowed', 'granted']):
            return 'Allowed'
        
        return None
    
    async def _generate_case_summary(self, doc: Dict, case_context: str) -> str:
        """Generate AI-powered case summary"""
        try:
            summary_query = (
                f"Generate a concise 2-sentence summary of this legal case: "
                f"Title: {doc.get('title', '')} "
                f"Headline: {doc.get('headline', '')} "
                f"Focus on key legal issues and relevance to current case context: {case_context}"
            )
            
            response = await self.run_tool("legal_knowledge_base", summary_query)
            return response[:200] + "..." if len(response) > 200 else response
            
        except Exception as e:
            logging.warning(f"Error generating case summary: {e}")
            return doc.get('headline', 'Case summary not available')[:150] + "..."
    
    async def _analyze_citations(self, top_cases: List[Dict]) -> Dict:
        """Analyze citation networks for top cases"""
        try:
            total_citations = 0
            authority_scores = []
            
            for case in top_cases[:3]:  # Analyze top 3 cases
                try:
                    doc_meta = await self.ik_client.get_document_metadata(case['tid'])
                    
                    cites = len(doc_meta.get('citeList', []))
                    cited_by = len(doc_meta.get('citedbyList', []))
                    
                    total_citations += cites + cited_by
                    
                    # Authority score based on court level and citations
                    court_weight = 10 if 'Supreme Court' in case['court'] else 7 if 'High Court' in case['court'] else 5
                    citation_weight = min(cited_by * 0.1, 3)  # Max 3 points from citations
                    authority_scores.append(court_weight + citation_weight)
                    
                except Exception as e:
                    logging.warning(f"Error analyzing citations for case {case['tid']}: {e}")
                    continue
            
            avg_authority = sum(authority_scores) / len(authority_scores) if authority_scores else 5.0
            
            return {
                'citation_count': total_citations,
                'authority_score': round(avg_authority, 1),
                'precedent_strength': 'High' if avg_authority > 8 else 'Medium' if avg_authority > 6 else 'Low'
            }
            
        except Exception as e:
            logging.error(f"Error in citation analysis: {e}")
            return {
                'citation_count': 0,
                'authority_score': 5.0,
                'precedent_strength': 'Medium'
            }
    
    def _generate_case_analytics(self, live_cases: List[Dict]) -> Dict:
        """Generate advanced case analytics"""
        if not live_cases:
            return {
                'conviction_rate': None,
                'legal_trends': 'Insufficient data for analysis',
                'success_patterns': [],
                'risk_factors': []
            }
        
        # Analyze outcomes
        outcomes = [case.get('case_outcome') for case in live_cases if case.get('case_outcome')]
        conviction_rate = len([o for o in outcomes if o == 'Conviction']) / len(outcomes) if outcomes else None
        
        # Identify patterns
        success_patterns = []
        risk_factors = []
        
        # Court analysis
        supreme_cases = len([c for c in live_cases if 'Supreme Court' in c.get('court', '')])
        if supreme_cases > 0:
            success_patterns.append(f"Supreme Court precedents available ({supreme_cases} cases)")
        
        # BNS section analysis
        all_sections = []
        for case in live_cases:
            all_sections.extend(case.get('bns_sections', []))
        
        if all_sections:
            common_sections = list(set(all_sections))
            success_patterns.append(f"Common BNS sections: {', '.join(common_sections[:3])}")
        
        # Risk analysis
        if conviction_rate and conviction_rate > 0.7:
            risk_factors.append("High conviction rate in similar cases")
        
        return {
            'conviction_rate': round(conviction_rate, 2) if conviction_rate else None,
            'legal_trends': f"Analysis based on {len(live_cases)} similar cases",
            'success_patterns': success_patterns,
            'risk_factors': risk_factors
        }

# Update Agent Manager to include Live Cases Agent
class EnhancedAgentManager(AgentManager):
    """Enhanced Agent Manager with Grid 5 Live Cases Agent"""
    
    def __init__(self):
        super().__init__()
        # Add Live Cases Agent
        self.live_cases_agent = LiveCasesAgent(self.query_engines)
        self.agents["live_cases"] = self.live_cases_agent
    
    async def populate_dashboard_with_grid5(self, case_id: str, case_context: str) -> Dict[str, str]:
        """
        Populate dashboard including Grid 5 using hierarchical execution
        """
        try:
            # Run hierarchical execution for Grids 1-4
            grid_1_4_results = await self.populate_dashboard_hierarchical(case_id, case_context)
            
            # Extract Laws Agent output for Grid 5
            laws_output = grid_1_4_results.get("legal", "")
            
            # Run Grid 5 with enhanced context
            print(f"🔍 [TIER 5] Running Live Cases Agent with full legal context...")
            grid5_results = await self.live_cases_agent.search_and_analyze_cases(
                case_context, laws_output
            )
            
            # Combine all results
            all_results = {
                **grid_1_4_results,
                "live_cases": grid5_results
            }
            
            print(f"✅ Enhanced dashboard population completed with Grid 5 for case {case_id}")
            return all_results
            
        except Exception as e:
            print(f"❌ Error in enhanced dashboard execution: {e}")
            # Fallback to Grid 1-4 only
            return await self.populate_dashboard_hierarchical(case_id, case_context)

# Global Agent Manager Instance
# ---------------------------------------------
agent_manager = EnhancedAgentManager()
