from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from services.data_room_service import DataRoomService

router = APIRouter()
data_room_service = DataRoomService()

@router.post("/upload")
async def upload_document(
    business_id: str,
    file: UploadFile = File(...)
):
    try:
        content = await file.read()
        result = await data_room_service.upload_document(
            file_content=content,
            filename=file.filename,
            business_id=business_id,
            user_id="demo_user"
        )
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result['error'])
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list/{business_id}")
async def list_documents(business_id: str):
    try:
        documents = await data_room_service.list_documents(business_id)
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))