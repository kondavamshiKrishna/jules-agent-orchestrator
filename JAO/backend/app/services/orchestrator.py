import re
import os
import logging
import asyncio
from collections import OrderedDict

logger = logging.getLogger(__name__)

AGENT_MAP = {
    "pydan": "py_dan_backend",
    "rita": "react_rita_frontend",
    "oliver": "ops_oliver_devops",
    "tina": "test_tina_qa",
    "ada": "ada_architect",
    "vera": "vera_verifier",
    "priya": "priya_promptcraft",
    "omega": "omega_system_auditor",
    "syncer": "syncer_master",
    "onboard": "syncer_onboard"
}

ASSIGNMENT_PATTERN = re.compile(r'@([a-z_]+)', re.IGNORECASE)

# Simple in-memory LRU cache for remote files
FILE_CACHE = OrderedDict()
MAX_CACHE_SIZE = 100


class OrchestratorEngine:
    """
    The core of the JAO autonomous loop.
    The Orchestrator acts as the "Firm Manager," looking at the
    '.jao/task_board.md' and related dashboards in the GitHub repo to
    decide the next agent to spawn. It ignores chat text entirely.
    """

    @staticmethod
    async def fetch_remote_file(github_repo_id: str, file_path: str) -> str:
        """
        Fetches a file directly from the remote GitHub repository using the Jules SDK
        or GitHub API. For now, since the Jules SDK `read_file` is not fully mocked,
        we simulate checking if the file exists locally (if we are working on a local clone)
        or return None if it doesn't exist remotely.
        """
        cache_key = (github_repo_id, file_path)
        if cache_key in FILE_CACHE:
            FILE_CACHE.move_to_end(cache_key)
            return FILE_CACHE[cache_key]

        # In a fully productionized cloud environment, this would call:
        # client = get_jules_client()
        # return await client.repo.read_file(github_repo_id, file_path)

        # Prevent Path Traversal Vulnerability
        base_dir = os.path.realpath(os.getcwd())
        abs_path = os.path.realpath(file_path)

        try:
            safe_path = os.path.relpath(abs_path, base_dir)
            if os.path.commonpath([base_dir, abs_path]) != base_dir:
                logger.warning("Attempted path traversal detected: %s", safe_path)
                return None
        except ValueError as e:
            logger.error("Invalid path provided for fetching remote file: %s", type(e).__name__)
            return None

        content = None
        # Fallback to local clone path if running locally against the repo it's sitting in
        if os.path.exists(abs_path):
            try:
                def _read_file():
                    with open(abs_path, "r", encoding="utf-8") as f:
                        return f.read()
                content = await asyncio.to_thread(_read_file)
            except Exception as e:
                # Re-calculate safe_path if it fails above but exists locally (though unlikely)
                try:
                    safe_path = os.path.relpath(abs_path, base_dir)
                except ValueError:
                    safe_path = "local-file"
                logger.error("Failed to read local file %s: %s", safe_path, type(e).__name__)
                return None

        if content is not None:
            FILE_CACHE[cache_key] = content
            if len(FILE_CACHE) > MAX_CACHE_SIZE:
                FILE_CACHE.popitem(last=False)

        return content

    @staticmethod
    async def is_repo_initialized(github_repo_id: str) -> bool:
        """Check if the .jao folder exists in the remote repo."""
        content = await OrchestratorEngine.fetch_remote_file(github_repo_id, ".jao/task_board.md")
        return content is not None

    @staticmethod
    async def read_blackboard_state(github_repo_id: str) -> dict:
        """
        Reads the '.jao/task_board.md' file from the remote repo to determine the next assigned agent.
        It looks for the first uncompleted task that has an assignment.
        Example format: '- [ ] Implement feature X (Assigned to: @pydan)'
        """

        board_content = await OrchestratorEngine.fetch_remote_file(github_repo_id, ".jao/task_board.md")

        # If the task board doesn't exist remotely, we must bootstrap
        if not board_content:
            return {
                "next_agent": "syncer_onboard",
                "prompt": "Initialize the .jao/ directory, project map, and task board for this repository. Assign the first task to @ada.",
                "mode": "Start"
            }

        lines = board_content.splitlines()

        for line in lines:
            # Find the first uncompleted task
            if "- [ ]" in line:
                # Look for an assignment tag (e.g., '@pydan')
                assignment_match = ASSIGNMENT_PATTERN.search(line)
                if assignment_match:
                    tag = assignment_match.group(1).lower()

                    mapped_agent = AGENT_MAP.get(tag, tag)

                    # Extract the task description
                    try:
                        task_desc = line.split("- [ ]")[1].split("(Assigned")[0].strip()
                    except IndexError:
                        task_desc = line.split("- [ ]")[1].strip()

                    return {
                        "next_agent": mapped_agent,
                        "prompt": f"Task from board: {task_desc}\n\nRead your specific workspace folder in '.jao/workspace/' for detailed handovers, blueprints, or test reports from the previous agent. Update the task board when done.",
                        "mode": "Start"  # Fully autonomous, no interactive approval needed
                    }

        # If all tasks are completed or no agent is assigned
        return None


    @staticmethod
    async def check_and_read_blackboard(github_repo_id: str):
        """
        Fetches the board content once and determines both if the repo is initialized
        and the next uncompleted task on the blackboard.
        Returns a tuple: (is_initialized, next_step_dict)
        """
        board_content = await OrchestratorEngine.fetch_remote_file(github_repo_id, ".jao/task_board.md")

        if not board_content:
            return False, None

        lines = board_content.splitlines()

        for line in lines:
            if "- [ ]" in line:
                assignment_match = ASSIGNMENT_PATTERN.search(line)
                if assignment_match:
                    tag = assignment_match.group(1).lower()
                    mapped_agent = AGENT_MAP.get(tag, tag)

                    try:
                        task_desc = line.split("- [ ]")[1].split("(Assigned")[0].strip()
                    except IndexError:
                        task_desc = line.split("- [ ]")[1].strip()

                    return True, {
                        "next_agent": mapped_agent,
                        "prompt": f"Task from board: {task_desc}\n\nRead your specific workspace folder in '.jao/workspace/' for detailed handovers, blueprints, or test reports from the previous agent. Update the task board when done.",
                        "mode": "Start"
                    }

        return True, None

    @staticmethod
    async def get_context_injection(github_repo_id: str) -> str:
        """
        Loads the entire '.jao/project_map.md' and '.jao/task_board.md'
        from the remote repo to inject into the agent's prompt so they don't have to guess.
        """
        context = "=== JAO REPOSITORY STATE ===\n"

        # Concurrent fetch for optimization
        map_task = OrchestratorEngine.fetch_remote_file(github_repo_id, ".jao/project_map.md")
        board_task = OrchestratorEngine.fetch_remote_file(github_repo_id, ".jao/task_board.md")

        map_content, board_content = await asyncio.gather(map_task, board_task)

        if map_content:
            context += f"\n-- Project Map --\n{map_content}\n"

        if board_content:
            context += f"\n-- Task Board --\n{board_content}\n"

        return context
