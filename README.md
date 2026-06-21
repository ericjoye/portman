# portman

A zero-dependency CLI that finds and kills processes on localhost ports — no more `lsof -i :3000` → `kill -9` → repeat.

## Install

```bash
pip install portman
```

## Usage

```bash
portman list          # List all listening ports
portman find 3000     # Find what's using port 3000
portman kill 3000     # Kill process on port 3000
portman free          # Show free ports
```

## Requirements

Python 3.11+, stdlib only.
