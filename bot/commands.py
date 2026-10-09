from bot.rules import normalize_text
from datetime import datetime, timezone

YOUTUBE_URL = "https://www.youtube.com/@reshi-r%C3%B8m"
stream_started_at = None



def parse_command(text):
    """Return (name, args) for a chat command"""
    cleaned = normalize_text(text)
    if not cleaned.startswith("!"):
        return None
    parts = cleaned[1:].split()
    if not parts:
        return None
    return parts[0], parts[1:]


# Commands
def cmd_comms(username, args):
    """Every command the bot knows"""
    names = []
    for name in COMMANDS:
        names.append("!" + name)
    return "Commands: " + ", ".join(names)

def cmd_youtube(username, args):
    """Sends YT channel link"""
    return f"Enjoying the content? Then check out Reshi's Youtube Channel for more!: {YOUTUBE_URL}"



def handle_command(text, username):
    """Bot's replies in chat."""
    parsed = parse_command(text)
    if parsed is None:
        return None
    name, args = parsed
    command = COMMANDS.get(name)
    if command is None:
        return None
    return command(username, args)


def format_uptime(started_at, now):
    """Return how long the stream has been live."""
    seconds = int((now - started_at).total_seconds())
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    if hours > 0:
        return f"Live for {hours}h {minutes}m"
    return f"Live for {minutes}m"


def cmd_uptime(username, args):
    """Says how long stream's been live."""
    if stream_started_at is None:
        return "Currently Offline."
    return format_uptime(stream_started_at, datetime.now(timezone.utc))







COMMANDS = {
    "comms": cmd_comms,
    "youtube": cmd_youtube,
    "uptime": cmd_uptime,
}

