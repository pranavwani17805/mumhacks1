from .base_agent import BaseAgent, AgentResponse
from typing import List, Dict

class MatchAgent(BaseAgent):
    def __init__(self):
        super().__init__("match_agent")
        self.buyer_pool = self._initialize_buyer_pool()
    
    async def execute(self, task: Dict[str, Any]) -> AgentResponse:
        business_profile = task.get('business_profile', {})
        matches = self._find_matches(business_profile)
        
        return AgentResponse(
            success=True,
            message=f"{len(matches)} investors matched this week",
            data={
                'matches': matches,
                'match_count': len(matches),
                'recommendation_reason': "Based on sector fit and investment capacity"
            },
            next_actions=["View match details", "Initiate contact"]
        )
    
    def _find_matches(self, business_profile: Dict) -> List[Dict]:
        sector = business_profile.get('sector', '')
        valuation = business_profile.get('valuation', 0)
        
        matches = []
        for buyer in self.buyer_pool:
            score = self._calculate_match_score(buyer, business_profile)
            if score > 0.6:  # Threshold for good matches
                matches.append({
                    **buyer,
                    'match_score': round(score, 2),
                    'anonymized_id': f"BUYER_{buyer['id'][:8]}"
                })
        
        return sorted(matches, key=lambda x: x['match_score'], reverse=True)[:3]
    
    def _calculate_match_score(self, buyer: Dict, business: Dict) -> float:
        score = 0.0
        
        # Sector match
        if buyer['preferred_sectors'] and business.get('sector') in buyer['preferred_sectors']:
            score += 0.4
        
        # Valuation range match
        business_val = business.get('valuation', 0)
        if buyer['min_investment'] <= business_val <= buyer['max_investment']:
            score += 0.4
        
        # Location preference
        if buyer.get('preferred_locations') and business.get('location') in buyer['preferred_locations']:
            score += 0.2
        
        return min(score, 1.0)
    
    def _initialize_buyer_pool(self) -> List[Dict]:
        return [
            {
                'id': 'fund_001',
                'type': 'VC Fund',
                'name': 'Alpha Ventures',
                'preferred_sectors': ['Technology', 'Manufacturing', 'Services'],
                'min_investment': 5000000,
                'max_investment': 50000000,
                'preferred_locations': ['Bangalore', 'Mumbai', 'Delhi'],
                'description': 'Early-stage technology focused fund'
            },
            {
                'id': 'individual_001', 
                'type': 'Entrepreneur',
                'name': 'Raj Sharma',
                'preferred_sectors': ['Retail', 'Services'],
                'min_investment': 1000000,
                'max_investment': 15000000,
                'preferred_locations': ['Delhi', 'Chennai'],
                'description': 'Experienced business owner looking to expand'
            },
            {
                'id': 'corporate_001',
                'type': 'Corporate Investor',
                'name': 'Growth Corp',
                'preferred_sectors': ['Manufacturing', 'Technology'],
                'min_investment': 10000000,
                'max_investment': 100000000,
                'preferred_locations': ['All India'],
                'description': 'Strategic acquisitions for portfolio expansion'
            }
        ]