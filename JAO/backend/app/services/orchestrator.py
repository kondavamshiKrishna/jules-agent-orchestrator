import re
import os

class OrchestratorEngine:
    """
    The heart of the JAO loop. This class reads the text output from a completed 
    Jules agent session and parses it to understand what the next step should be.
    """
    
    @staticmethod
    def detect_inbox_files(session_id: str):
        """
        New Blackboard Logic: Checks the filesystem for agent-generated 
        proposals or reports that should trigger the next agent.
        """
        import os
        inbox_path = f"JAO/sessions/{session_id}/inbox"
        if not os.path.exists(inbox_path):
            return None
            
        files = os.listdir(inbox_path)
        if not files:
            return None
            
        # Priority: BLUEPRINT.md > IMPLEMENTATION.md > TEST_REPORT.md
        priority = ["BLUEPRINT.md", "IMPLEMENTATION.md", "TEST_REPORT.md"]
        for p_file in priority:
            if p_file in files:
                with open(os.path.join(inbox_path, p_file), "r", encoding="utf-8") as f:
                    content = f.read()
                return {
                    "source_file": p_file,
                    "content": content,
                    "next_agent": OrchestratorEngine._get_next_from_file(p_file, content)
                }
        return None

    @staticmethod
    def _get_next_from_file(filename: str, content: str):
        """Helper to decide who follows a specific document type."""
        if filename == "BLUEPRINT.md": return "priya_promptcraft" # Needs prompt engineering
        if filename == "IMPLEMENTATION.md": return "test_tina_qa" # Needs testing
        if filename == "TEST_REPORT.md": return "vera_verifier" # Needs final review
        return None

    async def spawn_next_with_context(self, session_id: str, current_file: str):
        """
        The Auto-Activation Engine.
        1. Reads the current file.
        2. Finds the next agent in the 'Baton-Pass' sequence.
        3. Spawns them with the file content injected.
        """
        inbox_file = os.path.join(f"JAO/sessions/{session_id}/inbox", current_file)
        with open(inbox_file, "r") as f:
            work_done = f.read()
            
        next_agent_tag = self._decide_next_agent(current_file)
        if not next_agent_tag:
            return "Task Complete ✅"
            
        print(f"🚀 Auto-Activating @{next_agent_tag} for Session {session_id}...")
        
        # This is where the Jules API call happens
        # client.sessions.create(
        #     prompt=f"PROCESS THIS HANDOVER:\n\n{work_done}",
        #     agent_id=next_agent_tag
        # )
        return f"Spawned @{next_agent_tag}"

    def _decide_next_agent(self, filename: str):
        if "A_BLUEPRINT" in filename: return "priya_promptcraft"
        if "B_PROMPT" in filename: return "py_dan_backend" # or rita
        if "C_LOG" in filename: return "test_tina_qa"
        if "D_REPORT" in filename: return "vera_verifier"
        return None

    @staticmethod
    def parse_handover(text: str):
        text_lower = text.lower()
        if "@priya" in text_lower:
            agent = "priya_promptcraft"
            mode = "Interactive Plan"
            if "plan for the new feature" in text_lower:
                return {"next_agent": agent, "prompt": "Please create a plan for the new feature.", "mode": mode}
            else:
                return {"next_agent": agent, "prompt": "review this architecture", "mode": mode}
        elif "@pydan" in text_lower:
            return {"next_agent": "py_dan_backend", "prompt": "Implement the login endpoint.", "mode": "Interactive Plan"}
        elif "@tina" in text_lower:
            agent = "test_tina_qa"
            mode = "Start"
            if "write tests" in text_lower:
                return {"next_agent": agent, "prompt": "Write tests for the login endpoint.", "mode": mode}
            elif "verify" in text_lower:
                return {"next_agent": agent, "prompt": "Test the new endpoint with pytest.", "mode": mode}
            else:
                return {"next_agent": agent, "prompt": "Use mock data for testing.", "mode": mode}
        return None
