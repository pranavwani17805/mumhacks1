import pandas as pd
import numpy as np
from .base_agent import BaseAgent, AgentResponse

class ValuationAgent(BaseAgent):
    def __init__(self):
        super().__init__("valuation_agent")
    
    async def execute(self, task: Dict[str, Any]) -> AgentResponse:
        financial_data = task.get('financial_data', {})
        
        try:
            valuation = self._calculate_valuation(financial_data)
            
            return AgentResponse(
                success=True,
                message=f"Your business is worth ~₹{valuation:,.2f} (3x EBITDA)",
                data={
                    'estimated_value': valuation,
                    'valuation_method': 'EBITDA Multiple',
                    'multiple_used': 3.0,
                    'currency': 'INR',
                    'revenue': financial_data.get('annual_revenue'),
                    'ebitda': financial_data.get('ebitda'),
                    'assets': financial_data.get('total_assets')
                },
                next_actions=["Proceed to listing", "Adjust financial inputs"]
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Valuation failed: {str(e)}",
                next_actions=["Review financial data", "Contact support"]
            )
    
    def _calculate_valuation(self, financial_data: Dict) -> float:
        revenue = financial_data.get('annual_revenue', 0)
        ebitda = financial_data.get('ebitda', revenue * 0.3)  # Default 30% margin
        assets = financial_data.get('total_assets', 0)
        
        # Simple valuation: 3x EBITDA + 70% of assets
        valuation = (ebitda * 3) + (assets * 0.7)
        
        return round(valuation, 2)