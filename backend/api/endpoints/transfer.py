from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.orchestrator import AgentOrchestrator

router = APIRouter()
orchestrator = AgentOrchestrator()

class TransferRequest(BaseModel):
    business_type: str

@router.post("/start-transfer")
async def start_transfer(request: TransferRequest):
    try:
        result = await orchestrator.execute_workflow(
            user_id="demo_user",
            action="start_transfer",
            data={"business_type": request.business_type}
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/checklist/{business_type}")
async def get_checklist(business_type: str):
    try:
        result = await orchestrator.execute_workflow(
            user_id="demo_user",
            action="start_transfer",
            data={"business_type": business_type}
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))