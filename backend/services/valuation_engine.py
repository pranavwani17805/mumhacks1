import pandas as pd
import numpy as np
from typing import Dict, Any

class ValuationEngine:
    def __init__(self):
        self.methods = {
            'ebitda_multiple': self._ebitda_multiple,
            'revenue_multiple': self._revenue_multiple,
            'asset_based': self._asset_based,
            'dcf': self._discounted_cash_flow
        }
    
    def calculate_valuation(self, financial_data: Dict[str, Any], method: str = 'auto') -> Dict[str, Any]:
        if method == 'auto':
            method = self._select_best_method(financial_data)
        
        if method not in self.methods:
            raise ValueError(f"Unknown valuation method: {method}")
        
        valuation_func = self.methods[method]
        result = valuation_func(financial_data)
        
        return {
            'estimated_value': result['value'],
            'method': method,
            'method_details': result.get('details', {}),
            'currency': 'INR',
            'confidence_score': result.get('confidence', 0.8)
        }
    
    def _ebitda_multiple(self, data: Dict) -> Dict:
        ebitda = data.get('ebitda', data.get('annual_revenue', 0) * 0.25)
        multiple = 3.0  # Industry standard multiple
        
        # Adjust multiple based on business factors
        if data.get('profit_margin', 0) > 0.3:
            multiple += 0.5
        if data.get('years_operation', 0) > 10:
            multiple += 0.5
        
        value = ebitda * multiple
        assets = data.get('total_assets', 0)
        
        # Add asset value
        total_value = value + (assets * 0.7)
        
        return {
            'value': total_value,
            'details': {
                'ebitda': ebitda,
                'multiple_used': multiple,
                'asset_contribution': assets * 0.7
            },
            'confidence': 0.85
        }
    
    def _revenue_multiple(self, data: Dict) -> Dict:
        revenue = data.get('annual_revenue', 0)
        multiple = 1.2  # Conservative multiple
        
        # Adjust based on growth and margins
        if data.get('profit_margin', 0) > 0.2:
            multiple += 0.3
        
        value = revenue * multiple
        
        return {
            'value': value,
            'details': {
                'revenue': revenue,
                'multiple_used': multiple
            },
            'confidence': 0.75
        }
    
    def _asset_based(self, data: Dict) -> Dict:
        assets = data.get('total_assets', 0)
        # Use 70% of asset value for liquidation scenario
        value = assets * 0.7
        
        return {
            'value': value,
            'details': {
                'total_assets': assets,
                'recovery_rate': 0.7
            },
            'confidence': 0.9
        }
    
    def _discounted_cash_flow(self, data: Dict) -> Dict:
        # Simplified DCF calculation
        cash_flow = data.get('ebitda', data.get('annual_revenue', 0) * 0.25)
        growth_rate = 0.05  # 5% growth assumption
        discount_rate = 0.12  # 12% discount rate
        terminal_growth = 0.02  # 2% terminal growth
        
        # 5-year projection
        years = 5
        present_value = 0
        
        for year in range(1, years + 1):
            future_cf = cash_flow * ((1 + growth_rate) ** year)
            discount_factor = (1 + discount_rate) ** year
            present_value += future_cf / discount_factor
        
        # Terminal value
        terminal_cf = cash_flow * ((1 + growth_rate) ** (years + 1))
        terminal_value = terminal_cf / (discount_rate - terminal_growth)
        present_terminal_value = terminal_value / ((1 + discount_rate) ** years)
        
        total_value = present_value + present_terminal_value
        
        return {
            'value': total_value,
            'details': {
                'cash_flow': cash_flow,
                'growth_rate': growth_rate,
                'discount_rate': discount_rate,
                'terminal_growth': terminal_growth
            },
            'confidence': 0.7
        }
    
    def _select_best_method(self, data: Dict) -> str:
        """Select the most appropriate valuation method based on available data"""
        has_ebitda = data.get('ebitda') is not None or data.get('annual_revenue') is not None
        has_assets = data.get('total_assets', 0) > 0
        
        if has_ebitda:
            return 'ebitda_multiple'
        elif has_assets:
            return 'asset_based'
        else:
            return 'revenue_multiple'