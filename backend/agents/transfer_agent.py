from .base_agent import BaseAgent, AgentResponse

class TransferAgent(BaseAgent):
    def __init__(self):
        super().__init__("transfer_agent")
        self.transfer_checklist = self._initialize_checklist()
    
    async def execute(self, task: Dict[str, Any]) -> AgentResponse:
        business_type = task.get('business_type', 'private_limited')
        checklist = self._get_relevant_checklist(business_type)
        
        return AgentResponse(
            success=True,
            message="PAN, Udyam, GST transfer steps ready",
            data={
                'checklist': checklist,
                'estimated_timeline': '4-6 weeks',
                'documents_required': self._get_required_docs(business_type),
                'business_type': business_type
            },
            next_actions=["Start document collection", "Schedule advisor call"]
        )
    
    def _initialize_checklist(self) -> Dict:
        return {
            'private_limited': [
                "PAN transfer application",
                "GST registration transfer", 
                "Udyam registration update",
                "Bank account transfer",
                "License transfers",
                "Employee PF/ESI transfer",
                "Property lease transfer",
                "Vendor contract updates"
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
    
    def _get_relevant_checklist(self, business_type: str) -> List[str]:
        return self.transfer_checklist.get(business_type, [])
    
    def _get_required_docs(self, business_type: str) -> List[str]:
        doc_map = {
            'private_limited': [
                "Sale agreement", "Board resolution", "PAN card copies",
                "GST registration certificate", "Udyam certificate",
                "Company incorporation documents", "Latest financial statements"
            ],
            'partnership': [
                "Partnership deed", "Sale agreement", "PAN card",
                "GST certificate", "Partners identity proof"
            ],
            'proprietorship': [
                "Sale agreement", "PAN card", "GST certificate",
                "Identity proof", "Address proof", "Business licenses"
            ]
        }
        return doc_map.get(business_type, ["Sale agreement", "Identity proof"])