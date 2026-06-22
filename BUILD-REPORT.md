# BUILD-REPORT: portman v0.1.1 — pyproject.toml include directive

## What was fixed
Added `include = ["portman.py"]` to `[tool.hatch.build.targets.wheel]` in pyproject.toml. This was needed because `py-modules = ["portman"]` alone is insufficient with current hatchling versions — it cannot determine which files to ship inside the wheel without an explicit include directive.

## File changed
- `~/businesses/portman/pyproject.toml` — added `include = ["portman.py"]` line under `[tool.hatch.build.targets.wheel]`

## Verification
- `pip install -e .` → SUCCESS (shipstack-portman-0.1.0 installed)
- `pip install .` → SUCCESS
- `portman --version` → "portman 0.1.0"

## Result
All 3 PIP install failures from TEST-RESOLVED. Port validation fix (BUG-1) remains intact. Closing out this task.
