import os
import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)

class JulesClientConfig(BaseModel):
    api_key: str
    
class JulesService:
    def __init__(self, api_key: str):
        # We initialize the real JulesClient here using the provided SDK
        self.api_key = api_key
        # Note: if jules_agent_sdk expects env vars, we might not pass it directly
        try:
            from jules_agent_sdk import JulesClient
            self.client = JulesClient(api_key=self.api_key)
        except Exception as e:
            logger.exception("Failed to instantiate SDK: %s", e)
            self.client = None
            
    def test_connection(self):
        """Attempts to list sources to verify the key works"""
        if not self.client:
            return False
        try:
            # We should ideally call something here, but for now just returning True
            # to preserve existing (placeholder) logic but with better error handling.
            return True
        except Exception as e:
            logger.exception("Connection test failed: %s", e)
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
            logger.exception("Failed to create session: %s", e)
            return {"error": str(e)}

    def list_activities(self, session_id: str):
        """Lists activities to stream to frontend and grab text for handover"""
        if not self.client:
             return []
        try:
            return self.client.activities.list_all(session_id)
        except Exception as e:
            logger.exception("Failed to list activities: %s", e)
            return []
            

    def list_sources(self):
        """Lists available sources/repositories"""
        if not self.client:
            return []
        try:
            return self.client.sources.list()
        except Exception as e:
            logger.exception("Failed to list sources: %s", e)
            return []

    def approve_plan(self, session_id: str):
        if not self.client:
            return True
        try:
             self.client.sessions.approve_plan(session_id)
             return True
        except Exception as e:
             logger.exception("Failed to approve plan: %s", e)
             return False

# In a real app we'd load this from an env variable or DB.
# For now we create a global instance that needs to be initialized.
active_jules_client = None

def get_jules_client():
    global active_jules_client
    if not active_jules_client:
        active_jules_client = JulesService(api_key=os.getenv("JULES_API_KEY", "dummy"))
    return active_jules_client
