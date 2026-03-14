import re

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
        
        # 0. Parse Rejection / Verification Failure (from @tina, @vera)
        # Expected format: "REJECTED: Send back to @pydan. Reason: ..."
        rejection_match = re.search(r'REJECTED:\s*Send back to @([a-z_]+)\.?\s*(?:Reason:\s*)?(.*?)(?:---|\Z)', output_text, re.DOTALL | re.IGNORECASE)
        if rejection_match:
            tag = rejection_match.group(1).lower()
            agent_map = {
                "pydan": "py_dan_backend",
                "rita": "react_rita_frontend",
                "oliver": "ops_oliver_devops",
                "tina": "test_tina_qa",
                "ada": "ada_architect",
                "vera": "vera_verifier"
            }
            mapped_agent = agent_map.get(tag, tag)
            reason = rejection_match.group(2).strip()

            return {
                "next_agent": mapped_agent,
                "prompt": f"Your previous work was rejected by verification. Please fix the following issues:\n{reason}",
                "mode": "Start", # Developers usually just start working on fixes
                "status": "HANDOVER_REJECTED"
            }

        # 1. Parse 'Handover for @Priya' (from audit agents)
        priya_match = re.search(r'(Handover for @Priya:|@priya\s*,)(.*?)(?:---|\Z)', output_text, re.DOTALL | re.IGNORECASE)
        if priya_match:
            return {
                "next_agent": "priya_promptcraft",
                "prompt": priya_match.group(2).strip(),
                "mode": "Interactive Plan",
                "status": "HANDOVER"
            }
            
        # 2. Parse Dev assignment from Priya
        assignment_match = re.search(r'Assigned to:.*?@([a-z_]+)', output_text, re.IGNORECASE)
        prompt_match = re.search(r'(?:Full Prompt for|Prompt for) @[a-z_]+:(.*?)(?:---|\Z)', output_text, re.DOTALL | re.IGNORECASE)
        
        if assignment_match and prompt_match:
            tag = assignment_match.group(1).lower()
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
                "mode": "Interactive Plan" if mapped_agent in ["py_dan_backend", "ada_architect", "priya_promptcraft"] else "Start",
                "status": "HANDOVER"
            }

        # 3. Parse 'How to Verify (for @tina)'
        tina_match = re.search(r'(?:How to Verify \(for @tina\)|How to Test \(for @tina\)):(.*?)(?:---|\Z)', output_text, re.DOTALL | re.IGNORECASE)
        if tina_match:
             return {
                "next_agent": "test_tina_qa",
                "prompt": tina_match.group(1).strip(),
                "mode": "Start",
                "status": "HANDOVER"
             }

        # 4. Parse explicit completion
        if "TASK COMPLETE" in output_text.upper() or "ALL TESTS PASS" in output_text.upper():
            return {
                "next_agent": None,
                "prompt": "",
                "mode": "Done",
                "status": "COMPLETED"
            }
             
        # 5. Fallback: No automated trigger found -> Agent failed to provide formatting
        return {
            "next_agent": None,
            "prompt": "",
            "mode": "Error",
            "status": "STALLED_NO_HANDOVER"
        }
