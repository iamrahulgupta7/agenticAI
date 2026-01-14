
# command_policy.py
# -----------------------------
# ALLOWED COMMAND PREFIXES
# -----------------------------
ALLOWED_COMMANDS = [
    "top",
    "htop",
    "ps",
    "pidstat",
    "uptime",
    "free",
    "vmstat",
    "df",
    "du",
    "lsblk",
    "mount",
    "iostat",
    "sar",
    "mpstat",
    "ss",
    "netstat",
    "ip",
    "ping",
    "traceroute",
    "journalctl",
    "systemctl status",
    "uname",
    "hostnamectl",
    "cat /proc",
    "tail",
    "head",
]
# -----------------------------
# BLOCKED COMMAND KEYWORDS
# -----------------------------
BLOCKED_COMMANDS = [
    "rm ",
    "reboot",
    "shutdown",
    "mkfs",
    "dd ",
    ":(){",
    "kill -9 1",
    "chmod 777",
    "chown",
    "iptables -F",
]
DISALLOWED_SHELL_CHARS = [
    "|", "&&", "||", ";", ">", "<", "`", "$(", ")"
]
# -----------------------------
# POLICY CHECK FUNCTION
# -----------------------------
def is_command_allowed(command: str) -> tuple[bool, str]:
    cmd = command.strip().lower()
    # ❌ Block shell operators
    for char in DISALLOWED_SHELL_CHARS:
        if char in cmd:
            return False, f"❌ Shell operator blocked: {char}"
    # ❌ Block dangerous commands
    for blocked in BLOCKED_COMMANDS:
        if blocked in cmd:
            return False, f"❌ Blocked by blacklist: {blocked}"
    # ✅ Allow only whitelisted prefixes
    if not any(cmd.startswith(allowed) for allowed in ALLOWED_COMMANDS):
        return False, "❌ Command not in allowed list"
    return True, "✅ Command allowed"
