# Portman — PyPI Store Listing

## Package Name
`shipstack-portman` (install: `pip install shipstack-portman`, run: `portman`)

## Short Description (max 512 chars)
A zero-dependency CLI that finds and kills processes on localhost ports. No more lsof → copy PID → kill -9. Just `portman kill 3000`.

## Long Description

### Stop Fighting Stuck Ports

You know the drill: your dev server won't start because port 3000 is taken. You run `lsof -i :3000`, squint at the output, copy the PID, run `kill -9 <PID>`, and hope you got the right one.

**Portman makes this a single command.**

```bash
portman kill 3000
```

That's it. Portman finds the process, shows you what it is, and kills it.

### Commands

| Command | What it does |
|---------|-------------|
| `portman list` | List all listening ports on localhost |
| `portman find 3000` | Show what process is using port 3000 |
| `portman kill 3000` | Kill the process on port 3000 |
| `portman free` | Show which common dev ports are free |

### Zero Dependencies

Portman uses only Python stdlib. No `psutil`, no `npm`, no system packages. If you have Python 3.11+, you're ready.

### Cross-Platform

Works on macOS, Linux, and Windows. Portman uses the right native tool for each OS (`lsof`, `netstat`, etc.) under the hood.

### Safe by Design

- Port validation (1–65535) prevents mistakes
- Shows process details before killing
- Graceful SIGTERM first, SIGKILL only if needed

### Install

```bash
pip install portman
```

### Requirements

- Python 3.11+
- That's it.

## Keywords
port, kill, process, localhost, developer-tools, cli, python, devops, lsof, stuck-port, port-manager, terminal, command-line

## Classifiers
- Development Status :: 4 - Beta
- Environment :: Console
- Intended Audience :: Developers
- License :: OSI Approved :: MIT License
- Operating System :: OS Independent
- Programming Language :: Python :: 3
- Programming Language :: Python :: 3.11
- Programming Language :: Python :: 3.12
- Programming Language :: Python :: 3.13
- Programming Language :: Python :: 3.14
- Topic :: Software Development :: Quality Assurance
- Topic :: System :: Systems Administration
- Topic :: Utilities
