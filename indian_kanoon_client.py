# ---------------------------------------------
# Indian Kanoon API Client
# Modern async client for Indian Kanoon API integration
# ---------------------------------------------

import os
import json
import time
import logging
import asyncio
from typing import Dict, List, Optional, Any
import aiohttp
import requests
from datetime import datetime, timedelta

class IndianKanoonClient:
    """
    Modern async client for Indian Kanoon API
    Provides intelligent querying, caching, and error handling
    """
    
    def __init__(self, api_token: Optional[str] = None, base_url: Optional[str] = None):
        self.api_token = api_token or os.getenv("INDIAN_KANOON_API_TOKEN")
        self.base_url = base_url or os.getenv("INDIAN_KANOON_BASE_URL", "https://api.indiankanoon.org")
        
        if not self.api_token:
            raise ValueError("Indian Kanoon API token is required. Set INDIAN_KANOON_API_TOKEN environment variable.")
        
        self.headers = {
            'Authorization': f'Token {self.api_token}',
            'Accept': 'application/json',
            'User-Agent': 'LegalPlatform-ReActAgent/1.0'
        }
        
        # Rate limiting and caching
        self.last_request_time = 0
        self.min_request_interval = 0.5  # 500ms between requests
        self.cache = {}
        self.cache_ttl = int(os.getenv("GRID5_CACHE_TTL", "3600"))  # 1 hour default
        
        self.logger = logging.getLogger(__name__)
    
    async def _rate_limit(self):
        """Implement rate limiting to respect API limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            await asyncio.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _get_cache_key(self, endpoint: str, params: Dict) -> str:
        """Generate cache key for request"""
        return f"{endpoint}:{json.dumps(params, sort_keys=True)}"
    
    def _is_cache_valid(self, cache_entry: Dict) -> bool:
        """Check if cache entry is still valid"""
        if not cache_entry:
            return False
        
        cache_time = cache_entry.get('timestamp', 0)
        return (time.time() - cache_time) < self.cache_ttl
    
    async def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make async HTTP request to Indian Kanoon API"""
        await self._rate_limit()
        
        # Check cache first
        cache_key = self._get_cache_key(endpoint, params or {})
        if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key]):
            self.logger.info(f"Cache hit for {endpoint}")
            return self.cache[cache_key]['data']
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=self.headers, json=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Cache the response
                        self.cache[cache_key] = {
                            'data': data,
                            'timestamp': time.time()
                        }
                        
                        self.logger.info(f"API call successful: {endpoint}")
                        return data
                    
                    elif response.status == 403:
                        error_msg = "API authentication failed. Check your Indian Kanoon API token."
                        self.logger.error(error_msg)
                        raise Exception(error_msg)
                    
                    elif response.status == 429:
                        error_msg = "API rate limit exceeded. Implementing backoff..."
                        self.logger.warning(error_msg)
                        await asyncio.sleep(2)  # Backoff
                        return await self._make_request(endpoint, params)  # Retry
                    
                    else:
                        error_msg = f"API request failed with status {response.status}"
                        self.logger.error(error_msg)
                        raise Exception(error_msg)
        
        except aiohttp.ClientError as e:
            error_msg = f"Network error in API request: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
    
    async def search_cases(self, query: str, doctypes: str = None, pagenum: int = 0, 
                          maxcases: int = None) -> Dict:
        """
        Search for cases using Indian Kanoon search API
        
        Args:
            query: Search query (can include BNS sections, keywords, operators)
            doctypes: Filter by document types (e.g., 'supremecourt,highcourts')
            pagenum: Page number (starts from 0)
            maxcases: Maximum number of cases to return
            
        Returns:
            Dict containing search results with cases, metadata
        """
        maxcases = maxcases or int(os.getenv("GRID5_MAX_CASES", "20"))
        
        params = {
            'formInput': query,
            'pagenum': pagenum
        }
        
        if doctypes:
            params['doctypes'] = doctypes
        
        endpoint = "/search/"
        
        try:
            result = await self._make_request(endpoint, params)
            
            # Limit results if needed
            if 'docs' in result and len(result['docs']) > maxcases:
                result['docs'] = result['docs'][:maxcases]
            
            return result
            
        except Exception as e:
            self.logger.error(f"Search failed for query '{query}': {e}")
            return {
                'docs': [],
                'found': 0,
                'error': str(e)
            }
    
    async def get_document(self, doc_id: int, maxcites: int = 5, maxcitedby: int = 5) -> Dict:
        """
        Get full document content by ID
        
        Args:
            doc_id: Document ID from search results
            maxcites: Maximum citations to include
            maxcitedby: Maximum cited-by references to include
            
        Returns:
            Dict containing full document content and citations
        """
        params = {}
        if maxcites > 0:
            params['maxcites'] = maxcites
        if maxcitedby > 0:
            params['maxcitedby'] = maxcitedby
        
        endpoint = f"/doc/{doc_id}/"
        
        try:
            return await self._make_request(endpoint, params)
        except Exception as e:
            self.logger.error(f"Document fetch failed for ID {doc_id}: {e}")
            return {'error': str(e)}
    
    async def get_document_fragment(self, doc_id: int, query: str) -> Dict:
        """
        Get relevant document fragments for a query
        
        Args:
            doc_id: Document ID
            query: Search query to highlight in fragments
            
        Returns:
            Dict containing relevant document fragments
        """
        params = {'formInput': query}
        endpoint = f"/docfragment/{doc_id}/"
        
        try:
            return await self._make_request(endpoint, params)
        except Exception as e:
            self.logger.error(f"Document fragment fetch failed for ID {doc_id}: {e}")
            return {'error': str(e)}
    
    async def get_document_metadata(self, doc_id: int) -> Dict:
        """
        Get document metadata including citations
        
        Args:
            doc_id: Document ID
            
        Returns:
            Dict containing document metadata
        """
        endpoint = f"/docmeta/{doc_id}/"
        
        try:
            return await self._make_request(endpoint)
        except Exception as e:
            self.logger.error(f"Document metadata fetch failed for ID {doc_id}: {e}")
            return {'error': str(e)}
    
    def construct_bns_query(self, bns_sections: List[str], keywords: List[str] = None, 
                           fact_patterns: List[str] = None) -> str:
        """
        Construct intelligent search query using BNS sections and context
        
        Args:
            bns_sections: List of BNS sections (e.g., ['304A', '338'])
            keywords: Additional keywords from case context
            fact_patterns: Fact patterns to include in search
            
        Returns:
            Optimized search query string
        """
        query_parts = []
        
        # Add BNS sections with OR logic
        if bns_sections:
            bns_query = " ORR ".join([f'"{section}"' for section in bns_sections])
            query_parts.append(f"({bns_query})")
        
        # Add keywords with AND logic
        if keywords:
            keyword_query = " ANDD ".join([f'"{kw}"' for kw in keywords if len(kw) > 2])
            if keyword_query:
                query_parts.append(keyword_query)
        
        # Add fact patterns
        if fact_patterns:
            for pattern in fact_patterns:
                if len(pattern) > 5:  # Only meaningful patterns
                    query_parts.append(f'"{pattern}"')
        
        return " ANDD ".join(query_parts) if query_parts else ""
    
    def get_court_hierarchy_filter(self, include_supreme: bool = True, 
                                  include_high: bool = True, 
                                  include_district: bool = False) -> str:
        """
        Get doctypes filter based on court hierarchy preferences
        
        Args:
            include_supreme: Include Supreme Court cases
            include_high: Include High Court cases  
            include_district: Include District Court cases
            
        Returns:
            Comma-separated doctypes string
        """
        doctypes = []
        
        if include_supreme:
            doctypes.append('supremecourt')
        
        if include_high:
            doctypes.extend([
                'delhi', 'bombay', 'kolkata', 'chennai', 'allahabad', 
                'andhra', 'gujarat', 'karnataka', 'kerala', 'madhyapradesh',
                'patna', 'punjab', 'rajasthan'
            ])
        
        if include_district:
            doctypes.append('delhidc')
        
        return ','.join(doctypes)
    
    async def intelligent_case_search(self, bns_sections: List[str], 
                                    case_context: str, 
                                    max_cases: int = 20) -> Dict:
        """
        Perform intelligent case search using BNS sections and context
        
        Args:
            bns_sections: BNS sections from Laws Agent
            case_context: Case description and context
            max_cases: Maximum cases to return
            
        Returns:
            Dict with enhanced search results and metadata
        """
        # Extract keywords from case context
        keywords = self._extract_keywords(case_context)
        fact_patterns = self._extract_fact_patterns(case_context)
        
        # Construct intelligent query
        query = self.construct_bns_query(bns_sections, keywords, fact_patterns)
        
        if not query:
            return {'docs': [], 'found': 0, 'error': 'No valid search terms constructed'}
        
        # Get court hierarchy filter (prioritize higher courts)
        doctypes = self.get_court_hierarchy_filter(
            include_supreme=True,
            include_high=True, 
            include_district=False
        )
        
        self.logger.info(f"Intelligent search query: {query}")
        self.logger.info(f"Court filter: {doctypes}")
        
        # Perform search
        results = await self.search_cases(query, doctypes, maxcases=max_cases)
        
        # Add metadata
        results['search_metadata'] = {
            'bns_sections': bns_sections,
            'extracted_keywords': keywords,
            'fact_patterns': fact_patterns,
            'search_query': query,
            'court_filter': doctypes,
            'timestamp': datetime.now().isoformat()
        }
        
        return results
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from case context"""
        # Simple keyword extraction - can be enhanced with NLP
        import re
        
        # Common legal keywords to prioritize
        legal_keywords = [
            'negligence', 'malpractice', 'assault', 'murder', 'theft', 'fraud',
            'medical', 'surgical', 'accident', 'injury', 'death', 'evidence',
            'witness', 'investigation', 'criminal', 'civil', 'damages'
        ]
        
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [word for word in words if word in legal_keywords and len(word) > 3]
        
        return list(set(keywords))[:5]  # Top 5 unique keywords
    
    def _extract_fact_patterns(self, text: str) -> List[str]:
        """Extract fact patterns from case context"""
        # Simple pattern extraction - can be enhanced with NLP
        patterns = []
        
        # Look for common fact patterns
        if 'medical' in text.lower() and 'negligence' in text.lower():
            patterns.append('medical negligence')
        
        if 'surgical' in text.lower():
            patterns.append('surgical procedure')
        
        if 'accident' in text.lower():
            patterns.append('accident case')
        
        return patterns[:3]  # Top 3 patterns

# Global client instance
_client_instance = None

def get_indian_kanoon_client() -> IndianKanoonClient:
    """Get singleton Indian Kanoon client instance"""
    global _client_instance
    if _client_instance is None:
        _client_instance = IndianKanoonClient()
    return _client_instance
