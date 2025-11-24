from typing import List, Dict, Any
from sqlalchemy.orm import Session
from models.business import Business, BusinessListing

class ListingService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_listing(self, business_id: int, listing_data: Dict[str, Any]) -> BusinessListing:
        listing = BusinessListing(
            business_id=business_id,
            asking_price=listing_data.get('asking_price'),
            assets_included=listing_data.get('assets_included', []),
            transfer_timeline=listing_data.get('transfer_timeline'),
            handover_type=listing_data.get('handover_type', 'Immediate')
        )
        
        self.db.add(listing)
        self.db.commit()
        self.db.refresh(listing)
        
        # Update business status
        business = self.db.query(Business).filter(Business.id == business_id).first()
        if business:
            business.is_listed = True
            self.db.commit()
        
        return listing
    
    def get_business_listings(self, business_id: int) -> List[BusinessListing]:
        return self.db.query(BusinessListing).filter(
            BusinessListing.business_id == business_id
        ).all()
    
    def update_listing_status(self, listing_id: int, status: str) -> BusinessListing:
        listing = self.db.query(BusinessListing).filter(BusinessListing.id == listing_id).first()
        if listing:
            listing.status = status
            self.db.commit()
            self.db.refresh(listing)
        return listing
    
    def increment_views(self, listing_id: int) -> None:
        listing = self.db.query(BusinessListing).filter(BusinessListing.id == listing_id).first()
        if listing:
            listing.views_count += 1
            self.db.commit()