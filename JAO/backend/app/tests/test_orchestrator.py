import unittest
from unittest.mock import patch
import asyncio

from app.services.orchestrator import OrchestratorEngine

class TestOrchestrator(unittest.TestCase):
    def test_parse_handover_priya_v1(self):
        text = "Some audit results here. Handover for @Priya: Please update the prompt for better results. --- End of report."
        result = OrchestratorEngine.parse_handover(text)
        self.assertEqual(result, {
            "next_agent": "priya_promptcraft",
            "prompt": "Please update the prompt for better results.",
            "mode": "Interactive Plan"
        })

    def test_parse_handover_priya_v2(self):
        text = "Audit findings complete. @priya, analyze the technical debt in the backend. --- More info."
        result = OrchestratorEngine.parse_handover(text)
        self.assertEqual(result, {
            "next_agent": "priya_promptcraft",
            "prompt": "analyze the technical debt in the backend.",
            "mode": "Interactive Plan"
        })

    def test_parse_handover_assignment_pydan(self):
        text = "I have planned the feature. Assigned to: Py-Dan (@pydan). Full Prompt for @pydan: Implement the new API endpoint in `trade_routes.py`. --- Done."
        result = OrchestratorEngine.parse_handover(text)
        self.assertEqual(result, {
            "next_agent": "py_dan_backend",
            "prompt": "Implement the new API endpoint in `trade_routes.py`.",
            "mode": "Interactive Plan"
        })

    def test_parse_handover_assignment_rita(self):
        text = "The backend is ready. Assigned to: Rita (@rita). Prompt for @rita: Build the results table component. ---"
        result = OrchestratorEngine.parse_handover(text)
        self.assertEqual(result, {
            "next_agent": "react_rita_frontend",
            "prompt": "Build the results table component.",
            "mode": "Start"
        })

    def test_parse_handover_tina(self):
        text = "Code is committed. How to Verify (for @tina): Run `pytest` and check the logs for 200 OK responses. ---"
        result = OrchestratorEngine.parse_handover(text)
        self.assertEqual(result, {
            "next_agent": "test_tina_qa",
            "prompt": "Run `pytest` and check the logs for 200 OK responses.",
            "mode": "Start"
        })

    def test_parse_handover_none(self):
        text = "Just some random text with no handovers."
        result = OrchestratorEngine.parse_handover(text)
        self.assertIsNone(result)

    def test_parse_handover_empty(self):
        result = OrchestratorEngine.parse_handover("")
        self.assertIsNone(result)

    def test_parse_handover_case_insensitivity(self):
        text = "@PRIYA, do something."
        result = OrchestratorEngine.parse_handover(text)
        self.assertEqual(result["next_agent"], "priya_promptcraft")
        self.assertEqual(result["prompt"], "do something.")

    def test_parse_handover_mapping(self):
        tags = ["pydan", "rita", "oliver", "tina", "ada", "vera"]
        expected_agents = ["py_dan_backend", "react_rita_frontend", "ops_oliver_devops", "test_tina_qa", "ada_architect", "vera_verifier"]

        for tag, agent in zip(tags, expected_agents):
            text = f"Assigned to: @{tag}. Prompt for @{tag}: Test prompt."
            result = OrchestratorEngine.parse_handover(text)
            self.assertEqual(result["next_agent"], agent)


    def test_fetch_remote_file_error_path(self):
        """Verify that an exception during local file read returns None and logs the error."""
        test_exception = Exception("Disk Error")

        async def run_test():
            with patch("os.path.exists", return_value=True):
                with patch("builtins.open", side_effect=test_exception):
                    with patch("app.services.orchestrator.logger.exception") as mock_logger:
                        result = await OrchestratorEngine.fetch_remote_file("test-repo", ".jao/task_board.md")
                        self.assertIsNone(result)
                        mock_logger.assert_called_once_with("Failed to read local file %s: %s", ".jao/task_board.md", test_exception)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_test())

if __name__ == '__main__':
    unittest.main()
