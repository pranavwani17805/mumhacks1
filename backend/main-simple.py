from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List

app = FastAPI(title="Business Exit Platform", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ValuationRequest(BaseModel):
    financial_data: Dict[str, Any]

class ListingRequest(BaseModel):
    current_step: int
    user_data: Dict[str, Any]

class MatchRequest(BaseModel):
    business_profile: Dict[str, Any]

class TransferRequest(BaseModel):
    business_type: str

# Simple valuation calculation
def calculate_valuation(financial_data: Dict) -> Dict:
    revenue = financial_data.get('annual_revenue', 0)
    ebitda = financial_data.get('ebitda', revenue * 0.3)
    assets = financial_data.get('total_assets', 0)
    
    valuation = (ebitda * 3) + (assets * 0.7)
    
    return {
        'estimated_value': round(valuation, 2),
        'method': 'EBITDA Multiple',
        'multiple_used': 3.0,
        'currency': 'INR'
    }

# --- Document Management Endpoints ---

@app.post("/api/documents/upload")
async def upload_document(
    business_id: str,
    file: UploadFile = File(...)
):
    try:
        await file.read()
        
        return {
            'success': True,
            'filename': file.filename,
            'message': f'Document "{file.filename}" uploaded successfully to mock storage.'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mock upload failed: {str(e)}")

@app.get("/api/documents/list/{business_id}")
async def list_documents(business_id: str):
    mock_documents = [
        {
            "filename": "tax_return_2024.pdf",
            "uploaded_at": "2025-01-01T10:00:00Z",
            "size": 1024000, 
            "file_path": "/mock/path/tax_return_2024.pdf"
        },
        {
            "filename": "gst_statement_q3.xlsx",
            "uploaded_at": "2025-01-15T11:30:00Z",
            "size": 512000,
            "file_path": "/mock/path/gst_statement_q3.xlsx"
        }
    ]
    return {"documents": mock_documents}

# --- Valuation Routes ---

@app.post("/api/valuation/calculate")
async def valuation_calculate(request: ValuationRequest):
    result = calculate_valuation(request.financial_data)
    return {
        "success": True,
        "message": f"Your business is worth ~₹{result['estimated_value']:,.2f}",
        "data": result,
        "next_actions": ["Proceed to listing", "Adjust financial inputs"]
    }

# --- Transfer Routes ---

# Helper function to define the checklist (mimicking TransferAgent logic)
def _get_transfer_data(business_type: str) -> Dict:
    checklists = {
        'private_limited': [
            "PAN transfer application",
            "GST registration transfer", 
            "Udyam registration update",
            "Bank account transfer",
            "License transfers",
            "Employee PF/ESI transfer"
        ],
        'partnership': [
            "Partnership deed amendment",
            "PAN update",
            "GST registration transfer",
            "Bank account updates",
            "License transfers"
        ],
        'proprietorship': [
            "Business name transfer",
            "GST registration",
            "Shop establishment license",
            "Bank account changes",
            "Tax clearance certificate"
        ]
    }
    doc_map = {
        'private_limited': ["Sale agreement", "Board resolution", "PAN card copies", "Latest financial statements"],
        'partnership': ["Partnership deed", "Sale agreement", "PAN card"],
        'proprietorship': ["Sale agreement", "PAN card", "Business licenses"]
    }
    
    return {
        'checklist': checklists.get(business_type, []),
        'documents_required': doc_map.get(business_type, ["Sale agreement", "Identity proof"]),
        'estimated_timeline': '4-6 weeks',
        'business_type': business_type
    }

# NEW: GET endpoint to fetch the checklist (Frontend calls this)
@app.get("/api/transfer/checklist/{business_type}")
async def get_checklist(business_type: str):
    data = _get_transfer_data(business_type)
    return {
        "agent": "transfer",
        "result": "Checklist steps ready",
        "data": data,
        "next_actions": ["Start document collection", "Schedule advisor call"]
    }

# Existing POST endpoint
@app.post("/api/transfer/start-transfer")
async def start_transfer(request: TransferRequest):
    data = _get_transfer_data(request.business_type)
    
    return {
        "agent": "transfer",
        "result": "PAN, Udyam, GST transfer steps ready",
        "data": data,
        "next_actions": ["Start document collection", "Schedule advisor call"]
    }

# --- Listing Wizard Step Routes ---

class BusinessInfo(BaseModel):
    name: str
    sector: str
    location: str
    years_operation: int
    description: str

class FinancialInfo(BaseModel):
    annual_revenue: float
    ebitda: float
    total_assets: float
    profit_margin: float

class AssetInfo(BaseModel):
    equipment: List[str]
    property: List[str]
    intellectual_property: List[str]
    inventory: List[str]

class TransferInfo(BaseModel):
    timeline: str
    handover_type: str
    training_required: bool
    support_period: str

@app.post("/api/listing/step")
async def listing_step(request: ListingRequest):
    steps = [
        "Business Basic Info",
        "Financial Documentation", 
        "Asset Inventory",
        "Transfer Preferences",
        "Final Review"
    ]
    
    if request.current_step >= len(steps):
        return {
            "success": True,
            "message": "Listing process completed!",
            "next_actions": ["Review matches", "Publish listing"]
        }
    
    guidance = {
        0: "Enter business sector, location, and basic details",
        1: "Upload GST returns to unlock full listing potential",
        2: "List all physical and intellectual property assets",
        3: "Specify preferred transfer timeline and handover type",
        4: "Review all information before publishing"
    }
    
    return {
        "success": True,
        "message": f"Step {request.current_step + 1}: {guidance.get(request.current_step, 'Proceed to next step')}",
        "data": {
            'current_step': request.current_step,
            'total_steps': len(steps),
            'step_name': steps[request.current_step]
        }
    }

@app.post("/api/listing/business-info")
async def save_business_info(info: BusinessInfo):
    return {
        "success": True,
        "message": "Business information saved successfully",
        "next_step": "financial_info",
        "data": info.dict()
    }

@app.post("/api/listing/financial-info")
async def save_financial_info(info: FinancialInfo):
    return {
        "success": True, 
        "message": "Financial information saved successfully",
        "next_step": "assets_info",
        "data": info.dict()
    }

@app.post("/api/listing/assets-info")
async def save_assets_info(info: AssetInfo):
    return {
        "success": True,
        "message": "Assets information saved successfully", 
        "next_step": "transfer_info",
        "data": info.dict()
    }

@app.post("/api/listing/transfer-info")
async def save_transfer_info(info: TransferInfo):
    return {
        "success": True,
        "message": "Transfer information saved successfully",
        "next_step": "review",
        "data": info.dict()
    }

@app.post("/api/listing/publish")
async def publish_listing():
    return {
        "success": True,
        "message": "Business listing published successfully!",
        "listing_id": "LIST_001",
        "status": "published",
        "next_actions": ["View listing", "Share with buyers"]
    }

# --- Other Routes ---

@app.post("/api/matching/find-buyers")
async def find_buyers(request: MatchRequest):
    matches = [
        {
            "id": "fund_001",
            "type": "VC Fund",
            "name": "Alpha Ventures",
            "match_score": 0.85,
            "anonymized_id": "BUYER_fund_001",
            "preferred_sectors": ["Technology", "Manufacturing"],
            "min_investment": 5000000,
            "max_investment": 50000000,
            "description": "Early-stage technology focused fund"
        },
        {
            "id": "individual_001", 
            "type": "Entrepreneur",
            "name": "Raj Sharma",
            "match_score": 0.72,
            "anonymized_id": "BUYER_individual_001",
            "preferred_sectors": ["Retail", "Services"],
            "min_investment": 1000000,
            "max_investment": 15000000,
            "description": "Experienced business owner looking to expand"
        }
    ]
    
    return {
        "agent": "match",
        "result": f"{len(matches)} investors matched this week",
        "data": {
            'matches': matches,
            'match_count': len(matches)
        }
    }


@app.get("/")
async def root():
    return {"message": "Business Exit Platform API - Minimal Version"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)