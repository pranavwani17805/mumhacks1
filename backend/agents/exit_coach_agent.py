from .base_agent import BaseAgent, AgentResponse

class ExitCoachAgent(BaseAgent):
    def __init__(self):
        super().__init__("exit_coach_agent")
        self.listing_steps = [
            "Business Basic Info",
            "Financial Documentation", 
            "Asset Inventory",
            "Transfer Preferences",
            "Final Review"
        ]
    
    async def execute(self, task: Dict[str, Any]) -> AgentResponse:
        current_step = task.get('current_step', 0)
        user_data = task.get('user_data', {})
        
        if current_step >= len(self.listing_steps):
            return AgentResponse(
                success=True,
                message="Listing process completed!",
                next_actions=["Review matches", "Publish listing"]
            )
        
        step_guidance = self._get_step_guidance(current_step, user_data)
        
        return AgentResponse(
            success=True,
            message=f"Step {current_step + 1}: {step_guidance}",
            data={
                'current_step': current_step,
                'total_steps': len(self.listing_steps),
                'step_name': self.listing_steps[current_step],
                'requirements': self._get_step_requirements(current_step)
            },
            next_actions=[f"Complete {self.listing_steps[current_step]}"]
        )
    
    def _get_step_guidance(self, step: int, user_data: Dict) -> str:
        guidance_map = {
            0: "Enter business sector, location, and basic details",
            1: "Upload GST returns to unlock full listing potential",
            2: "List all physical and intellectual property assets",
            3: "Specify preferred transfer timeline and handover type",
            4: "Review all information before publishing"
        }
        return guidance_map.get(step, "Proceed to next step")
    
    def _get_step_requirements(self, step: int) -> List[str]:
        requirements_map = {
            0: ["Business name", "Sector", "Location", "Years in operation"],
            1: ["2 years P&L statements", "GST returns", "Tax filings"],
            2: ["Equipment list", "Property details", "IP assets"],
            3: ["Transfer timeline", "Handover preferences", "Training requirements"],
            4: ["Final verification", "Terms acceptance"]
        }
        return requirements_map.get(step, [])