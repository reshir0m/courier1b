import pytest
from bot.rules import clean_username, normalize_text, contains_link, can_post_links, decide_action

TEST_TERMS = ["badword1", "badword2"]

@pytest.mark.parametrize("name, expected", [
    (" @Reshir0m ", "reshir0m"),
    ("viewer123", "viewer123"),
])
def test_clean_username(name, expected):
    assert clean_username(name) == expected

@pytest.mark.parametrize("text, expected", [
    ("  WWW.EXAMPLE.COM  ", "www.example.com"),
    ("@Reshi nice play!", "@reshi nice play!"),
])
def test_normalize_text(text, expected):
    assert normalize_text(text) == expected

@pytest.mark.parametrize("text, expected", [
    ("https://twitch.tv/someone", True),
    ("www.example.com", True),
    ("hey chat!", False),
])
def test_contains_link(text, expected):
    assert contains_link(text) == expected

@pytest.mark.parametrize("username, expected", [
    ("@Reshir0m", True),
    ("randomviewer", False),
])
def test_can_post_links(username, expected):
    assert can_post_links(username) == expected

@pytest.mark.parametrize("message, username, expected", [
    ("hey chat what's up", "randomviewer", "allow"),
    ("FOLLOW ME www.example.com", "randomviewer", "delete"),
    ("www.example.com", "@Reshir0m", "allow"),
    ("  WWW.EXAMPLE.COM  ", "randomviewer", "delete"),
    ("check out twitch.tv/someone", "randomviewer", "delete"),
    ("ok.come on chat", "randomviewer", "allow"),
    ("go to example.com.", "randomviewer", "delete"),
    ("my site is example.com!", "randomviewer", "delete"),
    ("bit.ly/abc123", "randomviewer", "delete"),
    ("wait... really?", "randomviewer", "allow"),
])
def test_decide_action_links(message, username, expected):
    action, reason = decide_action(message,username)
    assert action == expected

@pytest.mark.parametrize("message, expected", [
    ("you are a badword1", "ban"),
    ("BADWORD1!", "ban"),
    ("badword1 www.example.com", "ban"),
    ("badword1x is fine", "allow"),
    ("you're a badword1", "ban"),
    ("that's badword1's fault", "ban"),
    ("BADWORD1’S", "ban"),
])
def test_decide_action_blocklist(message, expected):
    action, reason = decide_action(message, "randomviewer", TEST_TERMS)
    assert action == expected