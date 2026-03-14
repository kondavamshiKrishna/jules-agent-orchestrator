import time
import sys
import os
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath("JAO/backend"))

# Mock out fastapi and pydantic stuff
sys.modules['fastapi'] = MagicMock()
sys.modules['pydantic'] = MagicMock()
sys.modules['app.models.api'] = MagicMock()

try:
    from app.routes.agents import list_agents
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)

def run_benchmark(iterations=10000):
    start = time.perf_counter()
    for _ in range(iterations):
        list_agents()
    end = time.perf_counter()
    return end - start

if __name__ == "__main__":
    duration = run_benchmark()
    print(f"Baseline Time for 10000 iterations: {duration:.4f} seconds")
