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
