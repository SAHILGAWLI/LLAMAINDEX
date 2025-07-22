# ---------------------------------------------
# Advanced Case Analytics Engine for Grid 5
# Comprehensive analysis of legal case patterns, outcomes, and trends
# ---------------------------------------------

import re
import logging
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import statistics

@dataclass
class CaseOutcome:
    """Structured case outcome data"""
    outcome_type: str  # 'conviction', 'acquittal', 'dismissed', 'allowed', 'pending'
    confidence: float
    reasoning: str
    sentence_details: Optional[str] = None

@dataclass
class JudgeMetrics:
    """Judge performance metrics"""
    judge_name: str
    total_cases: int
    conviction_rate: float
    average_sentence_length: Optional[float] = None
    specialization_areas: List[str] = None

@dataclass
class CourtMetrics:
    """Court performance and characteristics"""
    court_name: str
    court_level: str  # 'supreme', 'high', 'district', 'sessions'
    total_cases: int
    conviction_rate: float
    average_case_duration: Optional[float] = None
    case_types: Dict[str, int] = None

@dataclass
class LegalTrend:
    """Legal trend analysis"""
    trend_type: str
    time_period: str
    direction: str  # 'increasing', 'decreasing', 'stable'
    confidence: float
    description: str
    supporting_data: Dict[str, Any] = None

class CaseAnalyticsEngine:
    """
    Advanced analytics engine for legal case analysis
    Provides comprehensive insights into case patterns, outcomes, and trends
    """
    
    def __init__(self):
        # BNS section severity mapping
        self.bns_severity = {
            '302': 'high',      # Murder
            '376': 'high',      # Rape
            '420': 'medium',    # Cheating
            '304A': 'medium',   # Negligence causing death
            '323': 'low',       # Simple hurt
            '279': 'medium',    # Rash driving
            '498A': 'medium',   # Cruelty to women
            '406': 'medium',    # Criminal breach of trust
            '325': 'medium',    # Grievous hurt
            '338': 'low'        # Endangering life
        }
        
        # Court hierarchy weights for authority scoring
        self.court_weights = {
            'supreme': 10,
            'high': 7,
            'district': 5,
            'sessions': 4,
            'magistrate': 3,
            'tribunal': 6
        }
        
        # Outcome patterns for classification
        self.outcome_patterns = {
            'conviction': [
                r'\bconvicted?\b', r'\bguilty\b', r'\bsentenced?\b', 
                r'\bimprisonment\b', r'\bfine\b', r'\bpunishment\b'
            ],
            'acquittal': [
                r'\bacquitted?\b', r'\bnot guilty\b', r'\bdischarged?\b',
                r'\bexonerated?\b', r'\bcleared?\b'
            ],
            'dismissed': [
                r'\bdismissed?\b', r'\brejected?\b', r'\bdenied?\b',
                r'\bstruck down\b', r'\bquashed?\b'
            ],
            'allowed': [
                r'\ballowed?\b', r'\bgranted?\b', r'\baccepted?\b',
                r'\bupheld?\b', r'\bsustained?\b'
            ],
            'pending': [
                r'\bpending\b', r'\bunder consideration\b', r'\badjourned?\b',
                r'\bremanded?\b', r'\bstayed?\b'
            ]
        }
    
    def analyze_case_outcomes(self, live_cases: List[Dict]) -> Dict[str, Any]:
        """
        Comprehensive analysis of case outcomes
        
        Args:
            live_cases: List of case dictionaries from Indian Kanoon
            
        Returns:
            Dict containing outcome analysis results
        """
        if not live_cases:
            return {
                'total_cases': 0,
                'outcome_distribution': {},
                'conviction_rate': None,
                'success_patterns': [],
                'risk_factors': []
            }
        
        outcomes = []
        outcome_counts = defaultdict(int)
        
        # Analyze each case outcome
        for case in live_cases:
            outcome = self._extract_case_outcome(case)
            outcomes.append(outcome)
            outcome_counts[outcome.outcome_type] += 1
        
        total_cases = len(live_cases)
        
        # Calculate conviction rate
        convictions = outcome_counts.get('conviction', 0)
        total_decided = sum(outcome_counts[k] for k in ['conviction', 'acquittal'])
        conviction_rate = convictions / total_decided if total_decided > 0 else None
        
        # Identify success patterns
        success_patterns = self._identify_success_patterns(live_cases, outcomes)
        
        # Identify risk factors
        risk_factors = self._identify_risk_factors(live_cases, outcomes, conviction_rate)
        
        return {
            'total_cases': total_cases,
            'outcome_distribution': dict(outcome_counts),
            'conviction_rate': conviction_rate,
            'success_patterns': success_patterns,
            'risk_factors': risk_factors,
            'outcome_details': outcomes
        }
    
    def analyze_court_performance(self, live_cases: List[Dict]) -> Dict[str, CourtMetrics]:
        """Analyze performance metrics by court"""
        court_data = defaultdict(lambda: {
            'cases': [],
            'outcomes': [],
            'case_types': defaultdict(int)
        })
        
        # Group cases by court
        for case in live_cases:
            court_name = case.get('court', 'Unknown Court')
            court_level = self._determine_court_level(court_name)
            
            court_data[court_name]['cases'].append(case)
            court_data[court_name]['level'] = court_level
            
            # Extract case type from BNS sections
            bns_sections = case.get('bns_sections', [])
            if bns_sections:
                primary_section = bns_sections[0]
                court_data[court_name]['case_types'][primary_section] += 1
            
            # Extract outcome
            outcome = self._extract_case_outcome(case)
            court_data[court_name]['outcomes'].append(outcome.outcome_type)
        
        # Calculate metrics for each court
        court_metrics = {}
        for court_name, data in court_data.items():
            total_cases = len(data['cases'])
            outcomes = data['outcomes']
            
            # Calculate conviction rate
            convictions = outcomes.count('conviction')
            total_decided = convictions + outcomes.count('acquittal')
            conviction_rate = convictions / total_decided if total_decided > 0 else 0.0
            
            court_metrics[court_name] = CourtMetrics(
                court_name=court_name,
                court_level=data['level'],
                total_cases=total_cases,
                conviction_rate=conviction_rate,
                case_types=dict(data['case_types'])
            )
        
        return court_metrics
    
    def analyze_legal_trends(self, live_cases: List[Dict], time_window_months: int = 24) -> List[LegalTrend]:
        """Analyze legal trends over time"""
        trends = []
        
        # BNS section trends
        bns_trend = self._analyze_bns_section_trends(live_cases)
        if bns_trend:
            trends.append(bns_trend)
        
        # Court preference trends
        court_trend = self._analyze_court_trends(live_cases)
        if court_trend:
            trends.append(court_trend)
        
        # Outcome trends
        outcome_trend = self._analyze_outcome_trends(live_cases)
        if outcome_trend:
            trends.append(outcome_trend)
        
        # Case complexity trends
        complexity_trend = self._analyze_complexity_trends(live_cases)
        if complexity_trend:
            trends.append(complexity_trend)
        
        return trends
    
    def calculate_case_authority_score(self, case: Dict, citation_data: Optional[Dict] = None) -> float:
        """
        Calculate authority score for a case based on multiple factors
        
        Factors:
        - Court level (Supreme > High > District)
        - Citation count
        - Case age (newer cases may have less established authority)
        - Judge reputation (if available)
        """
        score = 0.0
        
        # Court level weight (40% of score)
        court_name = case.get('court', '').lower()
        court_level = self._determine_court_level(court_name)
        court_weight = self.court_weights.get(court_level, 3)
        score += (court_weight / 10) * 4.0  # Max 4 points
        
        # Citation impact (30% of score)
        if citation_data:
            citation_count = citation_data.get('citation_count', 0)
            # Logarithmic scaling for citations
            citation_score = min(3.0, citation_count * 0.1)
            score += citation_score
        
        # Case similarity relevance (20% of score)
        similarity_score = case.get('similarity_score', 0.0)
        score += similarity_score * 2.0  # Max 2 points
        
        # BNS section severity (10% of score)
        bns_sections = case.get('bns_sections', [])
        if bns_sections:
            primary_section = bns_sections[0]
            severity = self.bns_severity.get(primary_section, 'medium')
            severity_score = {'high': 1.0, 'medium': 0.7, 'low': 0.4}.get(severity, 0.5)
            score += severity_score
        
        return min(10.0, score)  # Cap at 10.0
    
    def generate_strategic_recommendations(self, analytics_results: Dict) -> List[str]:
        """Generate strategic legal recommendations based on analytics"""
        recommendations = []
        
        outcome_analysis = analytics_results.get('outcome_analysis', {})
        court_metrics = analytics_results.get('court_metrics', {})
        trends = analytics_results.get('trends', [])
        
        # Conviction rate recommendations
        conviction_rate = outcome_analysis.get('conviction_rate')
        if conviction_rate is not None:
            if conviction_rate > 0.8:
                recommendations.append(
                    "⚠️ High conviction rate (>80%) in similar cases suggests strong prosecution evidence. "
                    "Focus on procedural defenses and evidence challenges."
                )
            elif conviction_rate < 0.3:
                recommendations.append(
                    "✅ Low conviction rate (<30%) in similar cases indicates potential defense opportunities. "
                    "Analyze successful defense strategies from acquitted cases."
                )
        
        # Court-specific recommendations
        supreme_court_cases = [c for c in court_metrics.values() if c.court_level == 'supreme']
        if supreme_court_cases:
            recommendations.append(
                f"📚 {len(supreme_court_cases)} Supreme Court precedent(s) available. "
                "These carry highest legal authority and should be prioritized in arguments."
            )
        
        # BNS section recommendations
        success_patterns = outcome_analysis.get('success_patterns', [])
        for pattern in success_patterns[:2]:  # Top 2 patterns
            recommendations.append(f"💡 Success Pattern: {pattern}")
        
        # Risk factor warnings
        risk_factors = outcome_analysis.get('risk_factors', [])
        for risk in risk_factors[:2]:  # Top 2 risks
            recommendations.append(f"⚠️ Risk Factor: {risk}")
        
        # Trend-based recommendations
        for trend in trends[:2]:  # Top 2 trends
            if trend.direction == 'increasing':
                recommendations.append(
                    f"📈 Legal Trend: {trend.description} is increasing. "
                    "Consider leveraging this trend in case strategy."
                )
        
        return recommendations[:6]  # Limit to top 6 recommendations
    
    def _extract_case_outcome(self, case: Dict) -> CaseOutcome:
        """Extract and classify case outcome"""
        text = f"{case.get('title', '')} {case.get('headline', '')} {case.get('summary', '')}".lower()
        
        # Check for explicit outcome in case data
        if case.get('case_outcome'):
            return CaseOutcome(
                outcome_type=case['case_outcome'].lower(),
                confidence=0.9,
                reasoning="Explicitly provided in case data"
            )
        
        # Pattern matching for outcome classification
        for outcome_type, patterns in self.outcome_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    confidence = 0.7 if len(re.findall(pattern, text, re.IGNORECASE)) > 1 else 0.6
                    return CaseOutcome(
                        outcome_type=outcome_type,
                        confidence=confidence,
                        reasoning=f"Pattern match: {pattern}"
                    )
        
        # Default to unknown
        return CaseOutcome(
            outcome_type='unknown',
            confidence=0.1,
            reasoning="No clear outcome pattern found"
        )
    
    def _determine_court_level(self, court_name: str) -> str:
        """Determine court hierarchy level"""
        court_lower = court_name.lower()
        
        if 'supreme' in court_lower:
            return 'supreme'
        elif 'high' in court_lower:
            return 'high'
        elif 'district' in court_lower:
            return 'district'
        elif 'sessions' in court_lower:
            return 'sessions'
        elif 'magistrate' in court_lower:
            return 'magistrate'
        elif 'tribunal' in court_lower:
            return 'tribunal'
        else:
            return 'unknown'
    
    def _identify_success_patterns(self, live_cases: List[Dict], outcomes: List[CaseOutcome]) -> List[str]:
        """Identify patterns in successful cases"""
        patterns = []
        
        # Successful outcomes (acquittals, dismissals, allowed appeals)
        successful_outcomes = ['acquittal', 'dismissed', 'allowed']
        successful_cases = [
            case for case, outcome in zip(live_cases, outcomes) 
            if outcome.outcome_type in successful_outcomes
        ]
        
        if not successful_cases:
            return patterns
        
        # Analyze successful case characteristics
        success_courts = [case.get('court', '') for case in successful_cases]
        court_counter = Counter(success_courts)
        
        if court_counter:
            top_court = court_counter.most_common(1)[0]
            if top_court[1] > 1:
                patterns.append(f"Higher success rate in {top_court[0]} ({top_court[1]} cases)")
        
        # BNS section analysis
        success_sections = []
        for case in successful_cases:
            success_sections.extend(case.get('bns_sections', []))
        
        section_counter = Counter(success_sections)
        if section_counter:
            top_section = section_counter.most_common(1)[0]
            if top_section[1] > 1:
                patterns.append(f"Section {top_section[0]} shows favorable outcomes ({top_section[1]} cases)")
        
        # High similarity cases
        high_similarity_success = [
            case for case in successful_cases 
            if case.get('similarity_score', 0) > 0.7
        ]
        if high_similarity_success:
            patterns.append(f"{len(high_similarity_success)} highly similar cases had favorable outcomes")
        
        return patterns
    
    def _identify_risk_factors(self, live_cases: List[Dict], outcomes: List[CaseOutcome], conviction_rate: Optional[float]) -> List[str]:
        """Identify risk factors from case analysis"""
        risks = []
        
        # High conviction rate risk
        if conviction_rate and conviction_rate > 0.7:
            risks.append(f"High conviction rate ({conviction_rate:.1%}) in similar cases")
        
        # Supreme Court precedents against
        unfavorable_outcomes = ['conviction']
        unfavorable_cases = [
            case for case, outcome in zip(live_cases, outcomes) 
            if outcome.outcome_type in unfavorable_outcomes
        ]
        
        supreme_unfavorable = [
            case for case in unfavorable_cases 
            if 'Supreme Court' in case.get('court', '')
        ]
        if supreme_unfavorable:
            risks.append(f"{len(supreme_unfavorable)} Supreme Court precedent(s) with unfavorable outcomes")
        
        # Consistent BNS section convictions
        conviction_sections = []
        for case, outcome in zip(live_cases, outcomes):
            if outcome.outcome_type == 'conviction':
                conviction_sections.extend(case.get('bns_sections', []))
        
        section_counter = Counter(conviction_sections)
        if section_counter:
            top_conviction_section = section_counter.most_common(1)[0]
            if top_conviction_section[1] > 2:
                risks.append(f"Section {top_conviction_section[0]} frequently results in conviction ({top_conviction_section[1]} cases)")
        
        return risks
    
    def _analyze_bns_section_trends(self, live_cases: List[Dict]) -> Optional[LegalTrend]:
        """Analyze trends in BNS section usage"""
        all_sections = []
        for case in live_cases:
            all_sections.extend(case.get('bns_sections', []))
        
        if not all_sections:
            return None
        
        section_counter = Counter(all_sections)
        most_common = section_counter.most_common(3)
        
        return LegalTrend(
            trend_type='bns_sections',
            time_period='recent_cases',
            direction='stable',
            confidence=0.7,
            description=f"Most frequently cited sections: {', '.join([s[0] for s in most_common])}",
            supporting_data={'section_counts': dict(section_counter)}
        )
    
    def _analyze_court_trends(self, live_cases: List[Dict]) -> Optional[LegalTrend]:
        """Analyze court preference trends"""
        courts = [case.get('court', '') for case in live_cases]
        court_counter = Counter(courts)
        
        if not court_counter:
            return None
        
        supreme_cases = sum(1 for court in courts if 'Supreme Court' in court)
        high_court_cases = sum(1 for court in courts if 'High Court' in court)
        
        if supreme_cases > high_court_cases:
            direction = 'increasing'
            description = "Higher representation of Supreme Court cases indicates strong precedential value"
        else:
            direction = 'stable'
            description = "Balanced distribution across court levels"
        
        return LegalTrend(
            trend_type='court_distribution',
            time_period='current_dataset',
            direction=direction,
            confidence=0.8,
            description=description,
            supporting_data={'court_counts': dict(court_counter)}
        )
    
    def _analyze_outcome_trends(self, live_cases: List[Dict]) -> Optional[LegalTrend]:
        """Analyze outcome trends"""
        outcomes = [self._extract_case_outcome(case).outcome_type for case in live_cases]
        outcome_counter = Counter(outcomes)
        
        if not outcome_counter:
            return None
        
        conviction_rate = outcome_counter.get('conviction', 0) / len(outcomes)
        
        if conviction_rate > 0.6:
            direction = 'increasing'
            description = f"High conviction rate ({conviction_rate:.1%}) suggests strong prosecution trends"
        elif conviction_rate < 0.3:
            direction = 'decreasing'
            description = f"Low conviction rate ({conviction_rate:.1%}) indicates defense-favorable trends"
        else:
            direction = 'stable'
            description = f"Balanced outcome distribution ({conviction_rate:.1%} conviction rate)"
        
        return LegalTrend(
            trend_type='case_outcomes',
            time_period='analyzed_cases',
            direction=direction,
            confidence=0.8,
            description=description,
            supporting_data={'outcome_distribution': dict(outcome_counter)}
        )
    
    def _analyze_complexity_trends(self, live_cases: List[Dict]) -> Optional[LegalTrend]:
        """Analyze case complexity trends"""
        complexity_scores = []
        
        for case in live_cases:
            # Calculate complexity based on multiple factors
            complexity = 0
            
            # Number of BNS sections
            bns_count = len(case.get('bns_sections', []))
            complexity += min(bns_count * 0.5, 2.0)
            
            # Document size (proxy for case complexity)
            doc_size = case.get('docsize', 0)
            if doc_size > 50000:  # Large document
                complexity += 1.0
            elif doc_size > 20000:  # Medium document
                complexity += 0.5
            
            # Court level (higher courts handle complex cases)
            court = case.get('court', '')
            if 'Supreme Court' in court:
                complexity += 1.5
            elif 'High Court' in court:
                complexity += 1.0
            
            complexity_scores.append(complexity)
        
        if not complexity_scores:
            return None
        
        avg_complexity = statistics.mean(complexity_scores)
        
        if avg_complexity > 3.0:
            direction = 'increasing'
            description = f"High case complexity (avg: {avg_complexity:.1f}) indicates sophisticated legal issues"
        elif avg_complexity < 1.5:
            direction = 'decreasing'
            description = f"Lower case complexity (avg: {avg_complexity:.1f}) suggests straightforward legal matters"
        else:
            direction = 'stable'
            description = f"Moderate case complexity (avg: {avg_complexity:.1f}) shows balanced case types"
        
        return LegalTrend(
            trend_type='case_complexity',
            time_period='analyzed_dataset',
            direction=direction,
            confidence=0.7,
            description=description,
            supporting_data={'average_complexity': avg_complexity, 'complexity_scores': complexity_scores}
        )

# Global analytics engine instance
_analytics_engine_instance = None

def get_case_analytics_engine() -> CaseAnalyticsEngine:
    """Get singleton case analytics engine instance"""
    global _analytics_engine_instance
    if _analytics_engine_instance is None:
        _analytics_engine_instance = CaseAnalyticsEngine()
    return _analytics_engine_instance
