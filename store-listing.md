# portman — PyPI / Developer Tool Listing

## Package Name

`portman-cli`

## Short Description

Find and kill processes on localhost ports. No more `lsof -i :3000` → `kill -9` → repeat.

## Long Description

portman is a zero-dependency CLI that finds and kills processes on localhost ports. Stop wasting time dealing with stale dev servers, forgotten Docker containers, and zombie Node/Python processes. One command to find what's using a port, and one command to kill it.

**WHY PORTMAN?**

Every developer wastes minutes per day dealing with "EADDRINUSE" errors. The current workflow is painful: `lsof -i :3000` → copy PID → `kill -9 12345` → hope you killed the right thing. On Windows it's even worse: `netstat -ano | findstr :3000` → `taskkill /PID 12345 /F`. portman makes it simple.

**CROSS-PLATFORM PORT MANAGEMENT**
`portman list` shows all listening ports with process names and PIDs on macOS, Linux, and Windows. `portman kill 3000` finds and kills the process on port 3000 with a confirmation prompt. `portman kill --all` cleans up all known dev server ports (3000, 3001, 5000, 8000, 8080, etc.) in one go.

**SMART FEATURES**
`portman find 3000` shows what's using a port without killing it. `portman free 3000` returns exit code 0 (free) or 1 (in use) — perfect for scripts. Manage a `~/.portmanrc` config file with custom port presets and ignore lists. All commands support `--json` output for automation.

**AI CODING AGENT FRIENDLY**
With AI coding agents (Claude Code, Codex, Cursor) spinning up servers automatically and leaving them running, portman is more essential than ever. Microservice development means more concurrent local servers than ever before.

## Key Features

- **List all listening ports** — with process names and PIDs (cross-platform)
- **Kill process by port** — with confirmation prompt
- **Kill all dev ports** — `--all` flag for common dev server ports
- **Find without killing** — `find` command for inspection
- **Check port availability** — `free` command with exit code 0/1
- **Config file** — `~/.portmanrc` for custom presets and ignore lists
- **JSON output** — `--json` flag on all commands for scripting
- **Zero dependencies** — Python 3.11+ stdlib (optional `psutil` for enhanced support)
- **Cross-platform** — macOS, Linux, Windows/WSL

## Installation

```bash
pip install portman-cli
```

Or with Homebrew:

```bash
brew install portman
```

## Requirements

- **Python:** 3.11+
- **Optional:** `psutil` for enhanced cross-platform support (`pip install psutil`)
- **No required dependencies** — stdlib only for core functionality

## Support

- **Contact:** eric@ericjoye.com
- **GitHub:** https://github.com/ericjoye/portman
- **Issues:** https://github.com/ericjoye/portman/issues
- **License:** MIT

## Keywords

port, localhost, kill process, cli, developer-tools, devops, command-line, python, cross-platform, zero-dependencies, EADDRINUSE, process management, dev server
