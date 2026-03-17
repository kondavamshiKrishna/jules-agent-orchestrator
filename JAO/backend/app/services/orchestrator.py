import re
import os

class OrchestratorEngine:
    """
    The heart of the JAO loop. This class reads the '.jao/task_board.md'
    to understand what the next step should be, fully relying on the filesystem state
    rather than brittle chat output regex parsing.
    """
    
    @staticmethod
    def parse_handover(output_text: str = ""):
        """
        Reads the '.jao/task_board.md' file to determine the next assigned agent.
        It looks for the first uncompleted task that has an assignment.
        Example task format: '- [ ] Implement feature X (Assigned to: @pydan)'
        """
        task_board_path = ".jao/task_board.md"
        if not os.path.exists(task_board_path):
            return None

        with open(task_board_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            # Look for an uncompleted task line: '- [ ]'
            if "- [ ]" in line:
                # Look for assignment: '@agent_tag'
                assignment_match = re.search(r'@([a-z_]+)', line, re.IGNORECASE)
                if assignment_match:
                    tag = assignment_match.group(1).lower()

                    # Map tag to full agent ID
                    agent_map = {
                        "pydan": "py_dan_backend",
                        "rita": "react_rita_frontend",
                        "oliver": "ops_oliver_devops",
                        "tina": "test_tina_qa",
                        "ada": "ada_architect",
                        "vera": "vera_verifier",
                        "priya": "priya_promptcraft",
                        "omega": "omega_system_auditor",
                        "syncer": "syncer_master"
                    }
                    mapped_agent = agent_map.get(tag, tag)

                    # Extract the task prompt
                    task_prompt = line.split("- [ ]")[1].strip()

                    return {
                        "next_agent": mapped_agent,
                        "prompt": f"Task from board: {task_prompt}\n\nRead your specific workspace folder in '.jao/workspace/' for detailed handovers or reports from the previous agent.",
                        "mode": "Interactive Plan" if mapped_agent in ["py_dan_backend", "ada_architect", "priya_promptcraft"] else "Start"
                    }

        # If no uncompleted tasks have an assigned agent
        return None

    @staticmethod
    def detect_inbox_files(session_id: str):
        # Legacy: No longer heavily used since we rely on `.jao/workspace/`
        pass

    async def spawn_next_with_context(self, session_id: str, current_file: str):
        pass
