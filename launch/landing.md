# Portman — Landing Page

## Headline
**Portman: Kill Stuck Ports in One Command**

## Subhead
A zero-dependency Python CLI that finds and kills processes on localhost ports. No more `lsof -i :3000` → `kill -9` → repeat.

## Benefit Bullets
- **Zero dependencies** — Uses only Python stdlib. No npm, no brew, no system packages. Works on any machine with Python 3.11+.
- **One command, done** — `portman kill 3000` finds the process, confirms, and kills it. No more copy-pasting PIDs from lsof output.
- **Developer-first design** — Lists all listening ports, finds what's using a specific port, shows free ports, and validates input so you never kill the wrong thing.

## CTA
```bash
pip install portman
```
Then run `portman list` to see what's running on your machine right now.

## FAQ

**Q: Does it work on Windows / Mac / Linux?**
A: Yes. Portman uses only Python stdlib (`socket`, `psutil`-free process lookup via `subprocess`), so it runs anywhere Python 3.11+ runs.

**Q: Is it safe? Will it kill the wrong process?**
A: Portman validates port numbers (1–65535) and shows you exactly what process it found before killing. It uses graceful termination first (SIGTERM), then SIGKILL only if needed.

**Q: Do I need to install anything else?**
A: No. Zero dependencies. Just `pip install portman` and you're done.

**Q: What if I don't have psutil?**
A: Portman doesn't need it. It uses native OS commands (`lsof` on macOS/Linux, `netstat` on Windows) under the hood.
