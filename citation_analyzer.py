# ---------------------------------------------
# Citation Network Analyzer for Grid 5
# Advanced citation analysis and precedent chain mapping
# ---------------------------------------------

import logging
import asyncio
from typing import List, Dict, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict, deque
import networkx as nx
from datetime import datetime

@dataclass
class CitationNode:
    """Represents a case in the citation network"""
    tid: int
    title: str
    court: str
    date: Optional[str]
    authority_score: float = 0.0
    in_degree: int = 0  # Times cited by others
    out_degree: int = 0  # Cases this cites
    precedent_strength: str = "Medium"
    
@dataclass
class CitationEdge:
    """Represents a citation relationship between cases"""
    citing_case: int  # TID of case that cites
    cited_case: int   # TID of case being cited
    citation_type: str = "direct"  # direct, indirect, distinguishing, overruling
    strength: float = 1.0

@dataclass
class PrecedentChain:
    """Represents a chain of legal precedents"""
    chain_id: str
    cases: List[CitationNode]
    total_authority: float
    chain_strength: str
    legal_principle: str
    
@dataclass
class CitationAnalysisResult:
    """Complete citation analysis results"""
    network_graph: Optional[nx.DiGraph] = None
    precedent_chains: List[PrecedentChain] = field(default_factory=list)
    authority_ranking: List[CitationNode] = field(default_factory=list)
    citation_clusters: Dict[str, List[int]] = field(default_factory=dict)
    network_metrics: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)

class CitationNetworkAnalyzer:
    """
    Advanced citation network analyzer for legal cases
    Builds and analyzes citation networks to identify precedent chains,
    authority patterns, and strategic legal insights
    """
    
    def __init__(self, indian_kanoon_client=None):
        self.ik_client = indian_kanoon_client
        self.citation_cache = {}  # Cache for citation data
        
        # Court authority weights
        self.court_authority = {
            'Supreme Court of India': 10.0,
            'Delhi High Court': 7.0,
            'Bombay High Court': 7.0,
            'Calcutta High Court': 7.0,
            'Madras High Court': 7.0,
            'Allahabad High Court': 7.0,
            'Karnataka High Court': 6.5,
            'Kerala High Court': 6.5,
            'Gujarat High Court': 6.5,
            'District Court': 4.0,
            'Sessions Court': 3.5,
            'Magistrate Court': 2.0
        }
    
    async def analyze_citation_network(self, live_cases: List[Dict], max_depth: int = 2) -> CitationAnalysisResult:
        """
        Perform comprehensive citation network analysis
        
        Args:
            live_cases: List of cases from Indian Kanoon
            max_depth: Maximum depth for citation chain analysis
            
        Returns:
            Complete citation analysis results
        """
        try:
            logging.info(f"Starting citation network analysis for {len(live_cases)} cases")
            
            # Step 1: Build citation nodes
            citation_nodes = await self._build_citation_nodes(live_cases)
            
            # Step 2: Fetch citation relationships
            citation_edges = await self._fetch_citation_relationships(citation_nodes, max_depth)
            
            # Step 3: Build network graph
            network_graph = self._build_network_graph(citation_nodes, citation_edges)
            
            # Step 4: Calculate authority scores
            authority_ranking = self._calculate_authority_scores(citation_nodes, network_graph)
            
            # Step 5: Identify precedent chains
            precedent_chains = self._identify_precedent_chains(network_graph, citation_nodes)
            
            # Step 6: Detect citation clusters
            citation_clusters = self._detect_citation_clusters(network_graph)
            
            # Step 7: Calculate network metrics
            network_metrics = self._calculate_network_metrics(network_graph)
            
            # Step 8: Generate strategic recommendations
            recommendations = self._generate_citation_recommendations(
                authority_ranking, precedent_chains, network_metrics
            )
            
            logging.info("Citation network analysis completed successfully")
            
            return CitationAnalysisResult(
                network_graph=network_graph,
                precedent_chains=precedent_chains,
                authority_ranking=authority_ranking,
                citation_clusters=citation_clusters,
                network_metrics=network_metrics,
                recommendations=recommendations
            )
            
        except Exception as e:
            logging.error(f"Error in citation network analysis: {e}")
            return CitationAnalysisResult(recommendations=[f"Citation analysis failed: {str(e)}"])
    
    async def _build_citation_nodes(self, live_cases: List[Dict]) -> Dict[int, CitationNode]:
        """Build citation nodes from live cases"""
        nodes = {}
        
        for case in live_cases:
            tid = case.get('tid', 0)
            if tid == 0:
                continue
                
            # Determine court authority weight
            court_name = case.get('court', 'Unknown Court')
            authority_weight = self._get_court_authority_weight(court_name)
            
            node = CitationNode(
                tid=tid,
                title=case.get('title', 'Unknown Case'),
                court=court_name,
                date=case.get('date'),
                authority_score=authority_weight,
                precedent_strength=self._determine_precedent_strength(authority_weight)
            )
            
            nodes[tid] = node
        
        return nodes
    
    async def _fetch_citation_relationships(self, nodes: Dict[int, CitationNode], max_depth: int) -> List[CitationEdge]:
        """Fetch citation relationships using Indian Kanoon API"""
        edges = []
        processed_tids = set()
        
        # Use BFS to explore citation network up to max_depth
        queue = deque([(tid, 0) for tid in nodes.keys()])
        
        while queue:
            current_tid, depth = queue.popleft()
            
            if depth >= max_depth or current_tid in processed_tids:
                continue
                
            processed_tids.add(current_tid)
            
            try:
                # Fetch citation data from Indian Kanoon
                if self.ik_client:
                    citation_data = await self._get_citation_data(current_tid)
                    
                    # Process cited cases (outgoing citations)
                    cited_cases = citation_data.get('citeList', [])
                    for cited_case in cited_cases[:10]:  # Limit to top 10 citations
                        cited_tid = cited_case.get('tid')
                        if cited_tid and cited_tid != current_tid:
                            edge = CitationEdge(
                                citing_case=current_tid,
                                cited_case=cited_tid,
                                citation_type='direct',
                                strength=1.0
                            )
                            edges.append(edge)
                            
                            # Add to queue for further exploration
                            if depth + 1 < max_depth:
                                queue.append((cited_tid, depth + 1))
                    
                    # Process citing cases (incoming citations)
                    citing_cases = citation_data.get('citedbyList', [])
                    for citing_case in citing_cases[:10]:  # Limit to top 10
                        citing_tid = citing_case.get('tid')
                        if citing_tid and citing_tid != current_tid:
                            edge = CitationEdge(
                                citing_case=citing_tid,
                                cited_case=current_tid,
                                citation_type='direct',
                                strength=1.0
                            )
                            edges.append(edge)
                
            except Exception as e:
                logging.warning(f"Error fetching citations for TID {current_tid}: {e}")
                continue
        
        return edges
    
    async def _get_citation_data(self, tid: int) -> Dict:
        """Get citation data with caching"""
        if tid in self.citation_cache:
            return self.citation_cache[tid]
        
        try:
            if self.ik_client:
                citation_data = await self.ik_client.get_document_metadata(tid)
                self.citation_cache[tid] = citation_data
                return citation_data
        except Exception as e:
            logging.warning(f"Failed to fetch citation data for TID {tid}: {e}")
        
        return {'citeList': [], 'citedbyList': []}
    
    def _build_network_graph(self, nodes: Dict[int, CitationNode], edges: List[CitationEdge]) -> nx.DiGraph:
        """Build NetworkX directed graph from nodes and edges"""
        G = nx.DiGraph()
        
        # Add nodes
        for tid, node in nodes.items():
            G.add_node(tid, **{
                'title': node.title,
                'court': node.court,
                'date': node.date,
                'authority_score': node.authority_score,
                'precedent_strength': node.precedent_strength
            })
        
        # Add edges
        for edge in edges:
            if edge.citing_case in G.nodes and edge.cited_case in G.nodes:
                G.add_edge(edge.citing_case, edge.cited_case, **{
                    'citation_type': edge.citation_type,
                    'strength': edge.strength
                })
        
        return G
    
    def _calculate_authority_scores(self, nodes: Dict[int, CitationNode], graph: nx.DiGraph) -> List[CitationNode]:
        """Calculate comprehensive authority scores using multiple metrics"""
        
        # Calculate PageRank for citation influence
        try:
            pagerank_scores = nx.pagerank(graph, weight='strength')
        except:
            pagerank_scores = {tid: 1.0 for tid in nodes.keys()}
        
        # Calculate in-degree and out-degree
        in_degrees = dict(graph.in_degree())
        out_degrees = dict(graph.out_degree())
        
        # Update node authority scores
        for tid, node in nodes.items():
            # Base court authority (40%)
            court_score = node.authority_score * 0.4
            
            # PageRank influence (30%)
            pagerank_score = pagerank_scores.get(tid, 0) * 10 * 0.3
            
            # Citation count (20%)
            in_degree = in_degrees.get(tid, 0)
            citation_score = min(in_degree * 0.5, 2.0) * 0.2
            
            # Network centrality (10%)
            try:
                centrality = nx.betweenness_centrality(graph).get(tid, 0)
                centrality_score = centrality * 10 * 0.1
            except:
                centrality_score = 0
            
            # Combined authority score
            node.authority_score = court_score + pagerank_score + citation_score + centrality_score
            node.in_degree = in_degree
            node.out_degree = out_degrees.get(tid, 0)
            
            # Update precedent strength
            node.precedent_strength = self._determine_precedent_strength(node.authority_score)
        
        # Sort by authority score
        return sorted(nodes.values(), key=lambda x: x.authority_score, reverse=True)
    
    def _identify_precedent_chains(self, graph: nx.DiGraph, nodes: Dict[int, CitationNode]) -> List[PrecedentChain]:
        """Identify important precedent chains in the citation network"""
        chains = []
        
        try:
            # Find strongly connected components
            strongly_connected = list(nx.strongly_connected_components(graph))
            
            # Find longest paths (precedent chains)
            for component in strongly_connected:
                if len(component) > 1:
                    subgraph = graph.subgraph(component)
                    
                    # Find the most authoritative path through this component
                    authority_nodes = sorted(
                        component, 
                        key=lambda x: nodes[x].authority_score if x in nodes else 0, 
                        reverse=True
                    )
                    
                    if len(authority_nodes) >= 2:
                        chain_nodes = [nodes[tid] for tid in authority_nodes[:5] if tid in nodes]
                        total_authority = sum(node.authority_score for node in chain_nodes)
                        
                        # Determine chain strength
                        avg_authority = total_authority / len(chain_nodes)
                        if avg_authority > 8.0:
                            chain_strength = "High"
                        elif avg_authority > 5.0:
                            chain_strength = "Medium"
                        else:
                            chain_strength = "Low"
                        
                        # Extract legal principle (simplified)
                        legal_principle = self._extract_legal_principle(chain_nodes)
                        
                        chain = PrecedentChain(
                            chain_id=f"chain_{len(chains)+1}",
                            cases=chain_nodes,
                            total_authority=total_authority,
                            chain_strength=chain_strength,
                            legal_principle=legal_principle
                        )
                        chains.append(chain)
            
            # Also identify simple citation chains (A cites B cites C)
            simple_chains = self._find_simple_citation_chains(graph, nodes)
            chains.extend(simple_chains)
            
        except Exception as e:
            logging.warning(f"Error identifying precedent chains: {e}")
        
        return sorted(chains, key=lambda x: x.total_authority, reverse=True)[:10]
    
    def _find_simple_citation_chains(self, graph: nx.DiGraph, nodes: Dict[int, CitationNode]) -> List[PrecedentChain]:
        """Find simple linear citation chains"""
        chains = []
        visited = set()
        
        for start_node in graph.nodes():
            if start_node in visited:
                continue
            
            # Follow citation chain forward
            chain_path = [start_node]
            current = start_node
            
            while True:
                successors = list(graph.successors(current))
                if not successors or len(successors) > 1:  # Stop at branching points
                    break
                
                next_node = successors[0]
                if next_node in chain_path:  # Avoid cycles
                    break
                
                chain_path.append(next_node)
                current = next_node
            
            # Create chain if it's significant
            if len(chain_path) >= 3:
                chain_nodes = [nodes[tid] for tid in chain_path if tid in nodes]
                if chain_nodes:
                    total_authority = sum(node.authority_score for node in chain_nodes)
                    
                    chain = PrecedentChain(
                        chain_id=f"simple_chain_{len(chains)+1}",
                        cases=chain_nodes,
                        total_authority=total_authority,
                        chain_strength="Medium",
                        legal_principle=self._extract_legal_principle(chain_nodes)
                    )
                    chains.append(chain)
                    
                    # Mark nodes as visited
                    visited.update(chain_path)
        
        return chains
    
    def _detect_citation_clusters(self, graph: nx.DiGraph) -> Dict[str, List[int]]:
        """Detect clusters of related cases in citation network"""
        clusters = {}
        
        try:
            # Use community detection algorithm
            undirected_graph = graph.to_undirected()
            communities = nx.community.greedy_modularity_communities(undirected_graph)
            
            for i, community in enumerate(communities):
                if len(community) >= 2:  # Only include meaningful clusters
                    clusters[f"cluster_{i+1}"] = list(community)
        
        except Exception as e:
            logging.warning(f"Error detecting citation clusters: {e}")
            # Fallback: simple clustering by court type
            court_clusters = defaultdict(list)
            for node_id in graph.nodes():
                node_data = graph.nodes[node_id]
                court = node_data.get('court', 'Unknown')
                court_clusters[court].append(node_id)
            
            clusters = {f"court_{court}": tids for court, tids in court_clusters.items() if len(tids) > 1}
        
        return clusters
    
    def _calculate_network_metrics(self, graph: nx.DiGraph) -> Dict[str, Any]:
        """Calculate comprehensive network metrics"""
        metrics = {}
        
        try:
            metrics['total_nodes'] = graph.number_of_nodes()
            metrics['total_edges'] = graph.number_of_edges()
            metrics['density'] = nx.density(graph)
            
            if graph.number_of_nodes() > 0:
                metrics['average_in_degree'] = sum(d for n, d in graph.in_degree()) / graph.number_of_nodes()
                metrics['average_out_degree'] = sum(d for n, d in graph.out_degree()) / graph.number_of_nodes()
                
                # Connectivity metrics
                if nx.is_weakly_connected(graph):
                    metrics['is_connected'] = True
                    metrics['diameter'] = nx.diameter(graph.to_undirected())
                else:
                    metrics['is_connected'] = False
                    metrics['connected_components'] = nx.number_weakly_connected_components(graph)
                
                # Centrality metrics
                try:
                    centrality = nx.betweenness_centrality(graph)
                    metrics['max_centrality'] = max(centrality.values()) if centrality else 0
                    metrics['avg_centrality'] = sum(centrality.values()) / len(centrality) if centrality else 0
                except:
                    metrics['max_centrality'] = 0
                    metrics['avg_centrality'] = 0
            
        except Exception as e:
            logging.warning(f"Error calculating network metrics: {e}")
            metrics['error'] = str(e)
        
        return metrics
    
    def _generate_citation_recommendations(self, authority_ranking: List[CitationNode], 
                                         precedent_chains: List[PrecedentChain], 
                                         network_metrics: Dict[str, Any]) -> List[str]:
        """Generate strategic recommendations based on citation analysis"""
        recommendations = []
        
        # Top authority cases
        if authority_ranking:
            top_case = authority_ranking[0]
            recommendations.append(
                f"🏛️ Highest Authority: {top_case.title} ({top_case.court}) - "
                f"Authority Score: {top_case.authority_score:.1f}/10"
            )
            
            supreme_cases = [case for case in authority_ranking if 'Supreme Court' in case.court]
            if supreme_cases:
                recommendations.append(
                    f"📚 {len(supreme_cases)} Supreme Court precedent(s) provide strongest legal authority"
                )
        
        # Precedent chain insights
        if precedent_chains:
            strongest_chain = precedent_chains[0]
            recommendations.append(
                f"⛓️ Strongest Precedent Chain: {len(strongest_chain.cases)} cases with "
                f"{strongest_chain.chain_strength} authority - {strongest_chain.legal_principle}"
            )
        
        # Network connectivity insights
        total_nodes = network_metrics.get('total_nodes', 0)
        if total_nodes > 5:
            density = network_metrics.get('density', 0)
            if density > 0.3:
                recommendations.append(
                    f"🔗 High Citation Density ({density:.2f}) indicates strong precedential relationships"
                )
            
            is_connected = network_metrics.get('is_connected', False)
            if is_connected:
                recommendations.append(
                    "🌐 Well-connected citation network provides comprehensive legal context"
                )
        
        # Citation frequency insights
        if authority_ranking:
            highly_cited = [case for case in authority_ranking if case.in_degree > 2]
            if highly_cited:
                recommendations.append(
                    f"📈 {len(highly_cited)} frequently cited case(s) indicate established legal principles"
                )
        
        return recommendations[:6]  # Limit to top 6 recommendations
    
    def _get_court_authority_weight(self, court_name: str) -> float:
        """Get authority weight for a court"""
        for court_key, weight in self.court_authority.items():
            if court_key.lower() in court_name.lower():
                return weight
        return 3.0  # Default weight for unknown courts
    
    def _determine_precedent_strength(self, authority_score: float) -> str:
        """Determine precedent strength based on authority score"""
        if authority_score >= 8.0:
            return "High"
        elif authority_score >= 5.0:
            return "Medium"
        else:
            return "Low"
    
    def _extract_legal_principle(self, chain_nodes: List[CitationNode]) -> str:
        """Extract legal principle from precedent chain (simplified)"""
        if not chain_nodes:
            return "Unknown legal principle"
        
        # Simple extraction based on case titles
        titles = [node.title.lower() for node in chain_nodes]
        
        # Common legal keywords
        if any('negligence' in title for title in titles):
            return "Medical/Professional Negligence Standards"
        elif any('murder' in title for title in titles):
            return "Criminal Liability and Intent"
        elif any('fraud' in title or 'cheating' in title for title in titles):
            return "Financial Fraud and Misrepresentation"
        elif any('accident' in title for title in titles):
            return "Accident Liability and Compensation"
        else:
            return "General Legal Precedent"

# Global citation analyzer instance
_citation_analyzer_instance = None

def get_citation_analyzer(indian_kanoon_client=None) -> CitationNetworkAnalyzer:
    """Get singleton citation analyzer instance"""
    global _citation_analyzer_instance
    if _citation_analyzer_instance is None:
        _citation_analyzer_instance = CitationNetworkAnalyzer(indian_kanoon_client)
    return _citation_analyzer_instance
