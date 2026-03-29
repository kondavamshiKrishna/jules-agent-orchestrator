import timeit
import os
import glob
from typing import List

class AgentPersona:
    def __init__(self, **kwargs):
        pass

def _load_personas_from_dir_old(
    directory: str, description_prefix: str, exclude_files: List[str] = None
):
    if exclude_files is None:
        exclude_files = []

    personas = []
    file_paths = [f"{directory}/test{i}.md" for i in range(100)]
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        if filename in exclude_files:
            continue
        personas.append(filename)
    return personas

def _load_personas_from_dir_new(
    directory: str, description_prefix: str, exclude_files: List[str] = None
):
    exclude_set = set(exclude_files) if exclude_files else set()

    personas = []
    file_paths = [f"{directory}/test{i}.md" for i in range(100)]
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        if filename in exclude_set:
            continue
        personas.append(filename)
    return personas

exclude_files = [f"test{i}.md" for i in range(100)]

old_time = timeit.timeit(lambda: _load_personas_from_dir_old("dir", "prefix", exclude_files), number=1000)
new_time = timeit.timeit(lambda: _load_personas_from_dir_new("dir", "prefix", exclude_files), number=1000)

print(f"Baseline (List lookup): {old_time:.4f}s")
print(f"Optimized (Set lookup): {new_time:.4f}s")
