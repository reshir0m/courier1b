LINK_POSTERS = ["reshir0m", "courier1b"]
DOMAIN_ENDINGS = [".com", ".tv", ".gg", ".net", ".org", ".io", ".co", ".ly"]
PUNCTUATION = ".,!?;:()[]\"'"

# Text cleanup
def normalize_text(text):
    """Return the message in lowercase, with spaces trimmed off both ends"""
    return text.strip().lower()


def clean_username(name):
    """Return the username lowercase. with spaces removed"""
    name = normalize_text(name)
    if name.startswith("@"):
        name = name[1:]  # slice: everything from index 1 on, which drops the @
    return name


# Links check
def contains_link(text):
    """Returns true if text looks like it contains a link."""
    words = text.split()
    for word in words:
        word = word.strip(PUNCTUATION)   # "example.com." -> "example.com"
        if word.startswith("http") or word.startswith("www."):
            return True
        for ending in DOMAIN_ENDINGS:
            if word.endswith(ending) or (ending+ "/") in word:
                return True
    return False



def can_post_links(username):
    """Return True if this user is permitted to post links"""
    return clean_username(username) in LINK_POSTERS



# Decides what Courier does with a message
def decide_action(text, username):
    """Return "delete" or "allow" for chat message. No side effects."""
    cleaned = normalize_text(text)
    has_link = contains_link(cleaned)
    if has_link and not can_post_links(username):
        return "delete"
    return "allow"



# Only prints if all checks passed
if __name__ == "__main__":
    
    def check(name, actual, expected):
        """Print a FAIL line if actual != expected. Return True if passed"""
        if actual == expected:
            return True
        print(f"FAILED: {name}: got {actual}, expected {expected}")
        return False
    
    
    
    results = [
        # Usernames
        check("clean_username drops @", clean_username(" @Reshir0m"), "reshir0m"),
        check("clean_username plain name", clean_username("viewer123"), "viewer123"),
        # Normalize text
        check("normalize_text lowercases", normalize_text("  WWW.EXAMPLE.COM  "), "www.example.com"),
        check("normalize_text keeps @", normalize_text("@Reshi nice play!"), "@reshi nice play!"),
        # Links
        check("contains_link finds https", contains_link("https://twitch.tv/someone"), True),
        check("contains_link finds www.", contains_link("www.example.com"), True),
        check("contains_link ignores plain chat", contains_link("hey, chat!"), False),
        # Permissions
        check("streamer can post links", can_post_links("@Reshir0m"), True),
        check("viewer can't post links", can_post_links("randomviewer"), False),
        # Decide action
        check("plain chat allowed", decide_action("hey chat what's up", "randomviewer"), "allow"),
        check("streamer link allowed", decide_action("www.example.com", "@Reshir0m"), "allow"),
        check("viewer link deleted", decide_action("FOLLOW ME www.example.com", "randomviewer"), "delete"),
        check("twitch.tv without https", decide_action("check out twitch.tv/someone", "randomviewer"), "delete"),
        check("ok.come is not a link", decide_action("ok.come on chat", "randomviewer"), "allow"),
        check("link at end of sentence", decide_action("go to example.com.", "randomviewer"), "delete"),
        check("link before punctuation", decide_action("my stire is example.com!", "randomviewer"), "delete"),
        check("link shortener", decide_action("bit.ly/abc123", "randomviewer"), "delete"),
        check("punctuation isn't a link", decide_action("wait... really?", "randomviewer"), "allow"),
        # any other asserts get converted the same way
    ]
    
    failed = results.count(False)
    if failed == 0:
        print("All checks passed!")
    else:
        print(f"{failed} check(s)")