#!/usr/bin/env python3
"""portman — A zero-dependency CLI that finds and kills processes on localhost ports.

Usage:
    portman list          Show all listening ports with process names and PIDs
    portman find <port>   Show what's using a port without killing it
    portman kill <port>   Find and kill the process on a given port
    portman free <port>   Check if a port is available (exit 0=free, 1=in use)
    portman config        Manage ~/.portmanrc configuration
    portman kill --all    Kill all known dev server ports
"""

import argparse
import json
import os
import platform
import signal
import socket
import subprocess
import sys
import textwrap
from pathlib import Path
from datetime import datetime

__version__ = "0.1.0"

# Common dev server ports
DEFAULT_DEV_PORTS = [3000, 3001, 4000, 5000, 5173, 8000, 8080, 8888, 9000, 9090]

# ANSI color codes
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    @classmethod
    def disable(cls):
        cls.RED = cls.GREEN = cls.YELLOW = cls.BLUE = ""
        cls.MAGENTA = cls.CYAN = cls.BOLD = cls.DIM = cls.RESET = ""


CONFIG_PATH = Path.home() / ".portmanrc"


def load_config():
    """Load ~/.portmanrc config file."""
    config = {
        "dev_ports": DEFAULT_DEV_PORTS,
        "ignore_pids": [],
    }
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.startswith("dev_ports="):
                        ports_str = line.split("=", 1)[1].strip()
                        config["dev_ports"] = [int(p.strip()) for p in ports_str.split(",") if p.strip()]
                    elif line.startswith("ignore_pids="):
                        pids_str = line.split("=", 1)[1].strip()
                        config["ignore_pids"] = [int(p.strip()) for p in pids_str.split(",") if p.strip()]
        except (ValueError, OSError):
            pass
    return config


def save_config(config):
    """Save config to ~/.portmanrc."""
    with open(CONFIG_PATH, "w") as f:
        f.write("# portman configuration\n")
        f.write(f"dev_ports={','.join(str(p) for p in config['dev_ports'])}\n")
        f.write(f"ignore_pids={','.join(str(p) for p in config['ignore_pids'])}\n")


def get_listening_ports():
    """Get all listening TCP ports with process info. Cross-platform."""
    system = platform.system()
    connections = []

    if system == "Linux":
        connections = _get_ports_linux()
    elif system == "Darwin":
        connections = _get_ports_macos()
    elif system == "Windows":
        connections = _get_ports_windows()
    else:
        # Fallback: try Linux method
        connections = _get_ports_linux()

    return connections


def _get_ports_linux():
    """Get listening ports on Linux by parsing /proc/net/tcp and /proc/net/tcp6."""
    connections = []
    seen = set()

    for proc_file in ["/proc/net/tcp", "/proc/net/tcp6"]:
        try:
            with open(proc_file) as f:
                lines = f.readlines()[1:]  # Skip header
                for line in lines:
                    parts = line.split()
                    if len(parts) < 10:
                        continue
                    local_address = parts[1]
                    state = parts[3]
                    inode = parts[9]

                    # State 0A = LISTEN
                    if state != "0A":
                        continue

                    # Parse local address (hex_ip:hex_port)
                    addr_parts = local_address.rsplit(":", 1)
                    if len(addr_parts) != 2:
                        continue
                    hex_ip, hex_port = addr_parts
                    port = int(hex_port, 16)

                    # Skip if we already have this port
                    if port in seen:
                        continue
                    seen.add(port)

                    # Find PID by searching /proc/*/fd for the inode
                    pid, process_name = _find_pid_by_inode(inode)

                    connections.append({
                        "port": port,
                        "pid": pid,
                        "process": process_name or "unknown",
                        "protocol": "tcp",
                    })
        except (OSError, ValueError):
            continue

    return connections


def _find_pid_by_inode(inode):
    """Find PID and process name by socket inode on Linux."""
    try:
        proc_dirs = os.listdir("/proc")
        for pid_str in proc_dirs:
            if not pid_str.isdigit():
                continue
            fd_dir = f"/proc/{pid_str}/fd"
            try:
                for fd in os.listdir(fd_dir):
                    try:
                        link = os.readlink(f"{fd_dir}/{fd}")
                        if f"socket:[{inode}]" in link:
                            # Get process name
                            try:
                                with open(f"/proc/{pid_str}/comm") as f:
                                    name = f.read().strip()
                            except OSError:
                                name = None
                            return int(pid_str), name
                    except OSError:
                        continue
            except PermissionError:
                continue
    except OSError:
        pass
    return None, None


def _get_ports_macos():
    """Get listening ports on macOS using lsof."""
    connections = []
    try:
        result = subprocess.run(
            ["lsof", "-iTCP", "-sTCP:LISTEN", "-P", "-n", "-F", "pcnT"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            return connections

        current = {}
        for line in result.stdout.splitlines():
            if not line:
                if current:
                    connections.append(current)
                    current = {}
                continue
            field_type = line[0]
            value = line[1:]
            if field_type == "p":
                current["pid"] = int(value)
            elif field_type == "c":
                current["process"] = value
            elif field_type == "n":
                # Parse address like *:3000 or 127.0.0.1:3000
                if ":" in value:
                    port_str = value.rsplit(":", 1)[1]
                    try:
                        current["port"] = int(port_str)
                    except ValueError:
                        pass

        if current:
            connections.append(current)

    except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
        pass

    # Normalize
    normalized = []
    seen = set()
    for conn in connections:
        port = conn.get("port")
        if port and port not in seen:
            seen.add(port)
            normalized.append({
                "port": port,
                "pid": conn.get("pid"),
                "process": conn.get("process", "unknown"),
                "protocol": "tcp",
            })

    return normalized


def _get_ports_windows():
    """Get listening ports on Windows using netstat."""
    connections = []
    try:
        result = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            return connections

        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 5 and parts[3] == "LISTENING":
                proto = parts[0]
                local = parts[1]
                pid_str = parts[-1]
                try:
                    port = int(local.rsplit(":", 1)[1])
                    pid = int(pid_str)
                except (ValueError, IndexError):
                    continue

                # Get process name from PID
                process_name = _get_process_name_windows(pid)

                connections.append({
                    "port": port,
                    "pid": pid,
                    "process": process_name or "unknown",
                    "protocol": proto.lower(),
                })
        return connections
    except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
        return []


def _get_process_name_windows(pid):
    """Get process name on Windows."""
    try:
        result = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.strip().split(",")
            if parts:
                return parts[0].strip('"')
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def _get_process_name(pid):
    """Get process name from PID (cross-platform)."""
    if not pid:
        return None
    system = platform.system()
    if system == "Linux":
        try:
            with open(f"/proc/{pid}/comm") as f:
                return f.read().strip()
        except OSError:
            return None
    elif system == "Darwin":
        try:
            result = subprocess.run(
                ["ps", "-p", str(pid), "-o", "comm="],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
    return None


def find_port(port):
    """Find what's using a specific port."""
    connections = get_listening_ports()
    for conn in connections:
        if conn["port"] == port:
            return conn
    return None


def is_port_free(port):
    """Check if a port is free by trying to bind to it."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False


def kill_process(pid, force=False):
    """Kill a process by PID."""
    if not pid:
        return False, "No PID provided"
    try:
        if force:
            os.kill(pid, signal.SIGKILL)
        else:
            os.kill(pid, signal.SIGTERM)
        return True, f"Process {pid} killed"
    except ProcessLookupError:
        return False, f"Process {pid} not found"
    except PermissionError:
        return False, f"Permission denied to kill {pid} (try sudo)"


def format_table(connections, use_color=True):
    """Format connections as a nice table."""
    if not connections:
        return "No listening ports found."

    # Header
    header = f"{'PORT':<10} {'PID':<10} {'PROCESS':<25} {'PROTOCOL':<8}"
    separator = "-" * len(header)
    lines = [header, separator]

    for conn in connections:
        port = conn["port"]
        pid = conn.get("pid") or "—"
        process = conn.get("process", "unknown")
        protocol = conn.get("protocol", "tcp")

        # Color dev ports
        port_str = str(port)
        if use_color and port in DEFAULT_DEV_PORTS:
            port_str = f"{Colors.YELLOW}{port_str}{Colors.RESET}"

        lines.append(f"{port_str:<10} {str(pid):<10} {process:<25} {protocol:<8}")

    return "\n".join(lines)


def cmd_list(args):
    """List all listening ports."""
    connections = get_listening_ports()

    if args.port:
        connections = [c for c in connections if c["port"] == args.port]

    if args.json:
        print(json.dumps(connections, indent=2))
        return

    if not connections:
        print("No listening ports found.")
        return

    # Sort by port
    connections.sort(key=lambda c: c["port"])

    print(f"\n{Colors.BOLD}Listening ports:{Colors.RESET}\n")
    print(format_table(connections))
    print(f"\n{Colors.DIM}Total: {len(connections)} listening port(s){Colors.RESET}\n")


def cmd_find(args):
    """Find what's using a specific port."""
    port = args.port
    conn = find_port(port)

    if args.json:
        if conn:
            print(json.dumps(conn, indent=2))
        else:
            print(json.dumps({"port": port, "status": "free"}, indent=2))
        return

    if conn:
        pid = conn.get("pid")
        process = conn.get("process", "unknown")
        print(f"\n{Colors.BOLD}Port {port}{Colors.RESET}")
        print(f"  PID:      {pid or 'unknown'}")
        print(f"  Process:  {process}")
        print(f"  Protocol: {conn.get('protocol', 'tcp')}")
        print()
    else:
        print(f"\n{Colors.GREEN}Port {port} is free{Colors.RESET}\n")


def cmd_kill(args):
    """Kill process on a port."""
    if args.all:
        config = load_config()
        dev_ports = config.get("dev_ports", DEFAULT_DEV_PORTS)
        killed = []
        failed = []

        for port in dev_ports:
            conn = find_port(port)
            if conn and conn.get("pid"):
                pid = conn["pid"]
                if not args.yes:
                    response = input(f"Kill {conn.get('process', 'unknown')} (PID {pid}) on port {port}? [y/N] ")
                    if response.lower() != "y":
                        continue
                success, msg = kill_process(pid, force=args.force)
                if success:
                    killed.append(port)
                else:
                    failed.append((port, msg))

        if args.json:
            print(json.dumps({"killed": killed, "failed": failed}, indent=2))
            return

        if killed:
            print(f"{Colors.GREEN}Killed processes on ports: {', '.join(str(p) for p in killed)}{Colors.RESET}")
        if failed:
            for port, msg in failed:
                print(f"{Colors.RED}Failed to kill port {port}: {msg}{Colors.RESET}")
        if not killed and not failed:
            print("No processes found on dev ports.")
        return

    port = args.port
    if not port:
        print("Error: specify a port or use --all")
        sys.exit(1)

    conn = find_port(port)

    if not conn:
        if args.json:
            print(json.dumps({"port": port, "status": "free"}, indent=2))
        else:
            print(f"{Colors.GREEN}Port {port} is free — nothing to kill{Colors.RESET}")
        return

    pid = conn.get("pid")
    process = conn.get("process", "unknown")

    if not pid:
        if args.json:
            print(json.dumps({"port": port, "error": "PID not found"}, indent=2))
        else:
            print(f"{Colors.YELLOW}Found process '{process}' on port {port} but could not determine PID{Colors.RESET}")
        return

    if not args.yes:
        response = input(f"Kill {process} (PID {pid}) on port {port}? [y/N] ")
        if response.lower() != "y":
            print("Aborted.")
            return

    success, msg = kill_process(pid, force=args.force)

    if args.json:
        if success:
            print(json.dumps({"port": port, "pid": pid, "status": "killed"}, indent=2))
        else:
            print(json.dumps({"port": port, "pid": pid, "error": msg}, indent=2))
        return

    if success:
        print(f"{Colors.GREEN}✓ Killed {process} (PID {pid}) on port {port}{Colors.RESET}")
    else:
        print(f"{Colors.RED}✗ {msg}{Colors.RESET}")
        sys.exit(1)


def cmd_free(args):
    """Check if a port is available."""
    port = args.port
    free = is_port_free(port)

    if args.json:
        print(json.dumps({"port": port, "free": free}, indent=2))
        return

    if free:
        print(f"{Colors.GREEN}✓ Port {port} is available{Colors.RESET}")
        sys.exit(0)
    else:
        print(f"{Colors.RED}✗ Port {port} is in use{Colors.RESET}")
        sys.exit(1)


def cmd_config(args):
    """Manage ~/.portmanrc configuration."""
    config = load_config()

    if args.json:
        print(json.dumps(config, indent=2))
        return

    if args.action == "show":
        print(f"\n{Colors.BOLD}portman config{Colors.RESET}")
        print(f"  Config file: {CONFIG_PATH}")
        print(f"  Dev ports: {', '.join(str(p) for p in config['dev_ports'])}")
        if config['ignore_pids']:
            print(f"  Ignore PIDs: {', '.join(str(p) for p in config['ignore_pids'])}")
        print()
    elif args.action == "init":
        if CONFIG_PATH.exists():
            print(f"Config already exists at {CONFIG_PATH}")
        else:
            save_config(config)
            print(f"{Colors.GREEN}Created config at {CONFIG_PATH}{Colors.RESET}")
    elif args.action == "add-port":
        if args.port not in config["dev_ports"]:
            config["dev_ports"].append(args.port)
            config["dev_ports"].sort()
            save_config(config)
            print(f"{Colors.GREEN}Added port {args.port} to dev ports{Colors.RESET}")
        else:
            print(f"Port {args.port} already in dev ports")
    elif args.action == "remove-port":
        if args.port in config["dev_ports"]:
            config["dev_ports"].remove(args.port)
            save_config(config)
            print(f"{Colors.GREEN}Removed port {args.port} from dev ports{Colors.RESET}")
        else:
            print(f"Port {args.port} not in dev ports")
    elif args.action == "reset":
        config = {"dev_ports": DEFAULT_DEV_PORTS, "ignore_pids": []}
        save_config(config)
        print(f"{Colors.GREEN}Reset config to defaults{Colors.RESET}")


def validate_port(value):
    """Validate port is in valid range 1-65535."""
    port = int(value)
    if port < 1 or port > 65535:
        raise argparse.ArgumentTypeError(f"port must be between 1 and 65535, got {port}")
    return port


def main():
    parser = argparse.ArgumentParser(
        prog="portman",
        description="A zero-dependency CLI that finds and kills processes on localhost ports.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
                portman list                    # List all listening ports
                portman find 3000               # Show what's using port 3000
                portman kill 3000               # Kill process on port 3000
                portman kill 3000 --force       # Force kill (SIGKILL)
                portman kill --all              # Kill all dev server ports
                portman free 3000               # Check if port 3000 is available
                portman config                  # Show current config
                portman config init             # Create ~/.portmanrc
                portman list --json             # JSON output for scripting
        """),
    )
    parser.add_argument("--version", action="version", version=f"portman {__version__}")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # list
    list_parser = subparsers.add_parser("list", help="List all listening ports")
    list_parser.add_argument("port", type=validate_port, nargs="?", help="Filter by specific port")

    # find
    find_parser = subparsers.add_parser("find", help="Find what's using a port")
    find_parser.add_argument("port", type=validate_port, help="Port to find")

    # kill
    kill_parser = subparsers.add_parser("kill", help="Kill process on a port")
    kill_parser.add_argument("port", type=validate_port, nargs="?", help="Port to kill")
    kill_parser.add_argument("--all", action="store_true", help="Kill all dev server ports")
    kill_parser.add_argument("--force", action="store_true", help="Force kill (SIGKILL)")
    kill_parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")

    # free
    free_parser = subparsers.add_parser("free", help="Check if a port is available")
    free_parser.add_argument("port", type=validate_port, help="Port to check")

    # config
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_sub = config_parser.add_subparsers(dest="action", help="Config action")
    config_sub.add_parser("show", help="Show current config")
    config_sub.add_parser("init", help="Create default config file")
    config_sub.add_parser("reset", help="Reset to defaults")
    add_port = config_sub.add_parser("add-port", help="Add a dev port")
    add_port.add_argument("port", type=validate_port, help="Port to add")
    remove_port = config_sub.add_parser("remove-port", help="Remove a dev port")
    remove_port.add_argument("port", type=validate_port, help="Port to remove")

    args = parser.parse_args()

    if args.no_color or args.json:
        Colors.disable()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Dispatch
    commands = {
        "list": cmd_list,
        "find": cmd_find,
        "kill": cmd_kill,
        "free": cmd_free,
        "config": cmd_config,
    }

    handler = commands.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
