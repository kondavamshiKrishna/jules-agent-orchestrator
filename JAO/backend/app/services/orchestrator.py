import re

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

    @staticmethod
    def parse_handover(output_text: str):
        # ... (existing regex logic for backwards compatibility)
        pass
