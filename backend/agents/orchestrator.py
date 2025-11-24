from typing import Dict, Any
from .valuation_agent import ValuationAgent
from .exit_coach_agent import ExitCoachAgent
from .match_agent import MatchAgent
from .transfer_agent import TransferAgent

class AgentOrchestrator:
    def __init__(self):
        self.agents = {
            'valuation': ValuationAgent(),
            'exit_coach': ExitCoachAgent(),
            'match': MatchAgent(),
            'transfer': TransferAgent()
        }
        self.workflow_state = {}
    
    async def execute_workflow(self, user_id: str, action: str, data: Dict[str, Any]):
        """Execute complete workflow based on user action"""
        
        if action == "start_valuation":
            return await self._handle_valuation(data)
        elif action == "create_listing":
            return await self._handle_listing(data)
        elif action == "find_buyers":
            return await self._handle_matching(data)
        elif action == "start_transfer":
            return await self._handle_transfer(data)
        else:
            return {"error": "Unknown action"}
    
    async def _handle_valuation(self, data: Dict) -> Dict:
        result = await self.agents['valuation'].execute(data)
        self.workflow_state['valuation'] = result.data
        
        return {
            'agent': 'valuation',
            'result': result.message,
            'data': result.data,
            'next_actions': result.next_actions
        }
    
    async def _handle_listing(self, data: Dict) -> Dict:
        # Include valuation data in context
        if 'valuation' in self.workflow_state:
            data['valuation_data'] = self.workflow_state['valuation']
        
        result = await self.agents['exit_coach'].execute(data)
        
        return {
            'agent': 'exit_coach', 
            'result': result.message,
            'data': result.data,
            'next_actions': result.next_actions
        }
    
    async def _handle_matching(self, data: Dict) -> Dict:
        # Combine business profile with existing data
        business_profile = {
            **data.get('business_profile', {}),
            'valuation': self.workflow_state.get('valuation', {}).get('estimated_value', 0)
        }
        
        match_data = {'business_profile': business_profile}
        result = await self.agents['match'].execute(match_data)
        
        return {
            'agent': 'match',
            'result': result.message,
            'data': result.data,
            'next_actions': result.next_actions
        }
    
    async def _handle_transfer(self, data: Dict) -> Dict:
        result = await self.agents['transfer'].execute(data)
        
        return {
            'agent': 'transfer',
            'result': result.message,
            'data': result.data,
            'next_actions': result.next_actions
        }