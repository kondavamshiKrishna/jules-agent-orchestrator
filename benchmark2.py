import time
import sys
import os
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath("JAO/backend"))

sys.modules['fastapi'] = MagicMock()
sys.modules['pydantic'] = MagicMock()
sys.modules['app.models.api'] = MagicMock()

from app.routes.agents import list_agents

start = time.perf_counter()
for _ in range(10000):
    list_agents()
end = time.perf_counter()
print(f"Time for 10000 iterations: {end - start:.4f} seconds")
