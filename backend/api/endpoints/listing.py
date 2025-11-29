from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

from agents.orchestrator import AgentOrchestrator
from services.listing_service import ListingService 
# from models.database import get_db # Assuming this dependency exists for DB connection

router = APIRouter()
orchestrator = AgentOrchestrator()

# --- Pydantic Models for Data Saving ---
# NOTE: Required fields are NOT optional by default. 
# Ensure the frontend sends data matching these types exactly.

class BusinessInfo(BaseModel):
    name: str
    sector: str
    location: str
    # This must be an INT! Empty strings from frontend will fail.
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

# --- API Endpoints ---

class ListingStepRequest(BaseModel):
    current_step: int
    user_data: Dict[str, Any]

class PublishRequest(BaseModel):
    business_id: int
    listing_data: Dict[str, Any]

@router.post("/step")
async def process_listing_step(request: ListingStepRequest):
    try:
        result = await orchestrator.execute_workflow(
            user_id="demo_user",
            action="create_listing",
            data={
                "current_step": request.current_step,
                "user_data": request.user_data
            }
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/publish")
async def publish_listing(request: PublishRequest):
    try:
        # DB saving logic with ListingService goes here in a full app
        return {
            "success": True,
            "message": "Business listing published successfully!",
            "listing_id": "LIST_001",
            "status": "published"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish listing: {str(e)}")

# --- Individual Step Saving Endpoints ---

@router.post("/business-info")
async def save_business_info(info: BusinessInfo):
    # This is the endpoint that was returning 422
    return {
        "success": True,
        "message": "Business information saved successfully",
        "next_step": "financial_info",
        "data": info.dict()
    }

@router.post("/financial-info")
async def save_financial_info(info: FinancialInfo):
    return {
        "success": True, 
        "message": "Financial information saved successfully",
        "next_step": "assets_info",
        "data": info.dict()
    }

@router.post("/assets-info")
async def save_assets_info(info: AssetInfo):
    return {
        "success": True,
        "message": "Assets information saved successfully", 
        "next_step": "transfer_info",
        "data": info.dict()
    }

@router.post("/transfer-info")
async def save_transfer_info(info: TransferInfo):
    return {
        "success": True,
        "message": "Transfer information saved successfully",
        "next_step": "review",
        "data": info.dict()
    }