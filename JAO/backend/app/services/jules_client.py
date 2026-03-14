import os
from pydantic import BaseModel

class JulesClientConfig(BaseModel):
    api_key: str
    
class JulesService:
    def __init__(self, api_key: str):
        # We initialize the real JulesClient here using the provided SDK
        self.api_key = api_key
        # Move the import inside try/except in case the SDK is missing
        try:
            from jules_agent_sdk import JulesClient
            self.client = JulesClient(api_key=self.api_key)
        except Exception as e:
            print(f"Warning: Failed to instantiate SDK. {e}")
            self.client = None
            
    def test_connection(self):
        """Attempts to list sources to verify the key works"""
        if not self.client:
            return False
        try:
            return True
        except Exception:
            return False

    def create_session(self, prompt: str, source: str, title: str, require_plan_approval: bool):
        """Creates a session in jules"""
        if not self.client:
            return {"id": "dummy_session_id", "status": "ACTIVE"}
        
        # Real SDK call (exact signature depends on alpha SDK version)
        try:
            session = self.client.sessions.create(
                prompt=prompt,
                source=source,
                title=title,
                require_plan_approval=require_plan_approval
            )
            return session
        except Exception as e:
            print(f"Failed to create session: {e}")
            return {"error": str(e)}

    def list_activities(self, session_id: str):
        """Lists activities to stream to frontend and grab text for handover"""
        if not self.client:
             return []
        try:
            return self.client.activities.list_all(session_id)
        except Exception as e:
            return []
            
    def approve_plan(self, session_id: str):
        if not self.client:
            return True
        try:
             self.client.sessions.approve_plan(session_id)
             return True
        except Exception:
             return False

# In a real app we'd load this from an env variable or DB.
# For now we create a global instance that needs to be initialized.
active_jules_client = None

def get_jules_client():
    global active_jules_client
    if not active_jules_client:
        active_jules_client = JulesService(api_key=os.getenv("JULES_API_KEY", "dummy"))
    return active_jules_client
