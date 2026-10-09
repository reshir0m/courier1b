import pytest
from bot.commands import parse_command, handle_command, format_uptime, YOUTUBE_URL, DISCORD_URL
from datetime import datetime, timedelta, timezone



@pytest.mark.parametrize("text, expected", [
    ("!comms", ("comms", [])),
    ("!COMMS", ("comms", [])),
    ("  !youtube  ", ("youtube", [])),
    ("!permit @Viewer123", ("permit", ["@viewer123"])),
    ("hey chat",None),
    ("!", None),
])
def test_parse_command(text, expected):
    assert parse_command(text) == expected


from bot.commands import parse_command, handle_command, YOUTUBE_URL


def test_comms_lists_commands():
    reply = handle_command("!comms", "viewer123")
    assert "!comms" in reply
    assert "!youtube" in reply


def test_youtube_gives_link():
    assert YOUTUBE_URL in handle_command("!youtube", "viewer123")


def test_discord_gives_link():
    assert DISCORD_URL in handle_command("!discord", "viewer123")


def test_commands_ignore_caps():
    assert YOUTUBE_URL in handle_command("!YouTube", "viewer123")


def test_unknown_command_ignored():
    assert handle_command("!notreal", "viewer123") is None


def test_plain_chat_ignored():
    assert handle_command("hey chat", "viewer123") is None


def test_uptime_hours_and_minutes():
    start = datetime(2026, 10, 8, 18, 0, tzinfo=timezone.utc)
    now = start + timedelta(hours=2, minutes=15)
    assert format_uptime(start, now) == "Live for 2h 15m"


def test_uptime_minutes_only():
    start = datetime(2026, 10, 8, 18, 0, tzinfo=timezone.utc)
    now = start +timedelta(minutes=45)
    assert format_uptime(start, now) == "Live for 45m"



def test_uptime_when_offline():
    assert handle_command("!uptime", "viewer123") == "Currently Offline."
