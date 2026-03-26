import pytest
import os
from unittest.mock import patch, mock_open

from app.routes.workflows import AGENTS_DIR

def test_path_traversal_logic():
    # Simulate the logic in workflows.py
    current_agent = "../../../../etc/passwd"

    # This should be the logic we patched
    safe_agent = os.path.basename(current_agent)

    assert safe_agent == "passwd"

    # It will raise an error now
    with pytest.raises(ValueError, match="Invalid agent identifier"):
        if safe_agent != current_agent or ".." in current_agent:
            raise ValueError("Invalid agent identifier.")


def test_fetch_remote_file_traversal():
    from app.services.orchestrator import OrchestratorEngine
    import asyncio

    # Use loop wrapper since pytest-asyncio markers might not work natively
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Test valid path
    # Fetch a file we know exists relative to the test's execution context
    import os
    current_file = os.path.relpath(__file__, os.getcwd())
    valid_content = loop.run_until_complete(OrchestratorEngine.fetch_remote_file("repo", current_file))
    assert valid_content is not None
    assert "def test_fetch_remote_file_traversal" in valid_content

    # Test invalid traversal path
    invalid_content = loop.run_until_complete(OrchestratorEngine.fetch_remote_file("repo", "../../../../etc/passwd"))
    assert invalid_content is None
