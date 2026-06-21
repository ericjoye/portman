# Screenshots — Portman

## Screenshot 1: Main Dashboard
```
┌─────────────────────────────────────────────────┐
│  Portman — Localhost Port Manager               │
├─────────────────────────────────────────────────┤
│  Port    Status    Process         PID          │
│  ─────────────────────────────────────────────── │
│  3000    ● Running  node (v20)     12345        │
│  5432    ● Running  postgres        6789         │
│  6379    ● Running  redis-server    1111         │
│  8080    ○ Free    —               —            │
│  8898    ● Running  python (mcp)    4449         │
│                                                 │
│  [Kill] [Restart] [Open Browser] [Copy Command] │
└─────────────────────────────────────────────────┘
```

## Screenshot 2: Port Details
```
┌─────────────────────────────────────────────────┐
│  Port 3000 — node                               │
├─────────────────────────────────────────────────┤
│  PID: 12345                                     │
│  Command: node server.js                        │
│  Started: 2026-06-20 14:30:22                  │
│  Uptime: 2h 15m                                 │
│  Memory: 45 MB                                  │
│                                                 │
│  [Kill Process] [View Logs] [Open in Browser]   │
└─────────────────────────────────────────────────┘
```

## Screenshot 3: CLI Mode
```
$ portman list
PORT    STATUS    PROCESS       PID
3000    RUNNING   node          12345
5432    RUNNING   postgres      6789
6379    RUNNING   redis-server  1111
8080    FREE      —             —

$ portman kill 3000
✓ Killed process 12345 on port 3000
```

## Notes for real screenshots
- Run `portman list` in terminal with dark background
- Show the web dashboard with multiple ports active
- Show the CLI in action with kill command
- Show the confirmation dialog before killing