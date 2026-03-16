import re
import os

class OrchestratorEngine:
    """
    The heart of the JAO loop. This class reads the text output from a completed 
    Jules agent session and parses it to understand what the next step should be.
    """
    
    @staticmethod
    def parse_handover(output_text: str):
        """
        Extracts handovers from the text.
        Returns a dictionary indicating the next agent and the prompt to pass to them.
        """

        # 1. Parse 'Handover for @Priya' (from audit agents)
        # Often formatted as "**@priya**, ..."
        priya_match = re.search(r'(Handover for @Priya:|@priya\s*,)(.*?)(?:---|\Z)', output_text, re.DOTALL | re.IGNORECASE)
        if priya_match:
            return {
                "next_agent": "priya_promptcraft",
                "prompt": priya_match.group(2).strip(),
                "mode": "Interactive Plan"
            }

        # 2. Parse Dev assignment from Priya
        # Often formatted as "Assigned to: [Name] (@tag)"
        assignment_match = re.search(r'Assigned to:.*?@([a-z_]+)', output_text, re.IGNORECASE)
        prompt_match = re.search(r'(?:Full Prompt for|Prompt for) @[a-z_]+:(.*?)(?:---|\Z)', output_text, re.DOTALL | re.IGNORECASE)

        if assignment_match and prompt_match:
            tag = assignment_match.group(1).lower()
            # Map tag to full agent ID
            agent_map = {
                "pydan": "py_dan_backend",
                "rita": "react_rita_frontend",
                "oliver": "ops_oliver_devops",
                "tina": "test_tina_qa",
                "ada": "ada_architect",
                "vera": "vera_verifier"
            }
            mapped_agent = agent_map.get(tag, tag)

            return {
                "next_agent": mapped_agent,
                "prompt": prompt_match.group(1).strip(),
                "mode": "Interactive Plan" if mapped_agent in ["py_dan_backend", "ada_architect", "priya_promptcraft"] else "Start"
            }

        # 3. Parse 'How to Verify (for @tina)' from developer agents
        tina_match = re.search(r'(?:How to Verify \(for @tina\)|How to Test \(for @tina\)):(.*?)(?:---|\Z)', output_text, re.DOTALL | re.IGNORECASE)
        if tina_match:
             return {
                "next_agent": "test_tina_qa",
                "prompt": tina_match.group(1).strip(),
                "mode": "Start"
             }

        # No automated trigger found
        return None


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
