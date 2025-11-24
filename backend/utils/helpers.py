import json
from datetime import datetime
from typing import Any, Dict

def format_currency(amount: float, currency: str = "INR") -> str:
    """Format currency in Indian numbering system"""
    if currency == "INR":
        return f"₹{amount:,.0f}"
    else:
        return f"{amount:,.2f}"

def serialize_model(model: Any) -> Dict:
    """Convert SQLAlchemy model to dictionary"""
    if hasattr(model, '__table__'):
        return {c.name: getattr(model, c.name) for c in model.__table__.columns}
    return {}

def validate_financial_data(data: Dict) -> bool:
    """Validate financial data inputs"""
    required_fields = ['annual_revenue']
    
    for field in required_fields:
        if field not in data or data[field] is None:
            return False
    
    # Validate numeric values
    try:
        float(data['annual_revenue'])
        if 'ebitda' in data and data['ebitda'] is not None:
            float(data['ebitda'])
        if 'total_assets' in data and data['total_assets'] is not None:
            float(data['total_assets'])
    except (ValueError, TypeError):
        return False
    
    return True