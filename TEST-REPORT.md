# TEST-REPORT: portman v0.1.1 — pip install + include directive

**Date:** 2026-06-21
**Tester:** tester (Hermes QA)
**Task:** t_99012562

## Summary

All 5 verification items PASS. The one-line `include = ["portman.py"]` fix in `[tool.hatch.build.targets.wheel]` resolves the previous "Unable to determine which files to ship inside the wheel" error.

## Test Results

| # | Test | Command | Result |
|---|------|---------|--------|
| 1 | `pip install -e .` (Python 3.11) | `/tmp/portman-test-venv-311/bin/pip install -e .` | PASS — Successfully installed shipstack-portman-0.1.0 |
| 2 | `pip install -e .` (Python 3.14) | `/tmp/portman-test-venv/bin/pip install -e .` | PASS — Successfully installed shipstack-portman-0.1.0 |
| 3 | `pip install .` (non-editable) | `/tmp/portman-test-venv/bin/pip install .` | PASS — Successfully built and installed wheel |
| 4 | `portman --version` | `portman --version` | PASS — Output: `portman 0.1.0` |
| 5 | Port validation (out-of-range) | `portman kill 99999` | PASS — Rejected with: "port must be between 1 and 65535, got 99999" (exit code 2) |
| 6 | `portman --help` | `portman --help` | PASS — Full help text displayed with all subcommands |

## Environment

- Python 3.11.15 (system, via venv)
- Python 3.14 (system, via venv)
- pip 24.0 / 26.1.1
- hatchling build backend
- WSL (Ubuntu)

## Verdict: **PASS**

The BUILDER's fix is minimal and correct. The `include = ["portman.py"]` directive explicitly tells hatchling which file to include in the wheel, resolving the auto-detection failure. All installation methods work, the CLI entry point is properly registered, and port validation still rejects out-of-range values.

Ready for launch preparation.
