import boto3
from botocore.exceptions import ClientError
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os
from config.settings import settings

class DataRoomService:
    def __init__(self):
        # For demo purposes, we'll use local storage
        # In production, use S3 or similar cloud storage
        self.base_path = "data_rooms"
        os.makedirs(self.base_path, exist_ok=True)
    
    async def upload_document(self, file_content: bytes, filename: str, 
                            business_id: str, user_id: str) -> Dict:
        try:
            # Create business-specific folder
            business_folder = os.path.join(self.base_path, str(business_id))
            os.makedirs(business_folder, exist_ok=True)
            
            # Generate unique filename
            file_extension = os.path.splitext(filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(business_folder, unique_filename)
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            return {
                'success': True,
                'file_path': file_path,
                'filename': filename,
                'unique_filename': unique_filename,
                'uploaded_at': datetime.now().isoformat(),
                'message': 'Document uploaded successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def generate_shareable_link(self, file_path: str, 
                                    recipient_id: str, 
                                    expiry_hours: int = 24) -> Dict:
        try:
            # In a real implementation, this would generate a presigned URL
            # For demo, we'll return a mock link
            expiry = datetime.now() + timedelta(hours=expiry_hours)
            
            return {
                'success': True,
                'shareable_link': f"/api/documents/shared/{uuid.uuid4()}",
                'expiry': expiry.isoformat(),
                'recipient': recipient_id
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def list_documents(self, business_id: str) -> List[Dict]:
        business_folder = os.path.join(self.base_path, str(business_id))
        if not os.path.exists(business_folder):
            return []
        
        documents = []
        for filename in os.listdir(business_folder):
            file_path = os.path.join(business_folder, filename)
            if os.path.isfile(file_path):
                stat = os.stat(file_path)
                documents.append({
                    'filename': filename,
                    'uploaded_at': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    'size': stat.st_size,
                    'file_path': file_path
                })
        
        return documents