LINK_POSTERS = ["reshir0m", "courier1b"]
DOMAIN_ENDINGS = [".com", ".tv", ".gg", ".net", ".org", ".io", ".co", ".ly"]
PUNCTUATION = ".,!?;:()[]\"'"

# Text cleanup
def normalize_text(text):
    """Return the message in lowercase, with spaces trimmed off both ends"""
    return text.strip().lower().replace("’", "'")


def clean_username(name):
    """Return the username lowercase. with spaces removed"""
    name = normalize_text(name)
    if name.startswith("@"):
        name = name[1:]  # slice: everything from index 1 on, which drops the @
    return name


# Links check
def contains_link(text):
    """Returns true if text looks like it contains a link."""
    for word in text.split():
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



# Blacklisted word check
def contains_blocked_term(text, blocked_terms):
    """Return True if any word in the ext is in blocked_terms"""
    for word in text.split():  # "you are a badword1!" -> ["you", "are", "a", "badword1"]
        word = word.strip(PUNCTUATION)  # "badword1!" -> "badword1"
        word = word.split("'")[0]
        if word in blocked_terms:   # is this exact word on the list?
            return True
    return False



# Decides what Courier does with a message
def decide_action(text, username, blocked_terms=()):
    """Return "ban", "delete" or "allow" for chat message. No side effects."""
    cleaned = normalize_text(text)
    if contains_blocked_term(cleaned, blocked_terms):
        return "ban", "used a blocked term"
    if contains_link(cleaned) and not can_post_links(username):
        return "delete"
    return "allow"

def carry_out(action, username, reason):
    """Acts on verdict. The only function with side effects."""
    if action == "ban":
        print(f"Banned {username}: {reason}")
    elif action == "delete":
        print(f"Deleted a message from {username}: {reason}")


# Only prints if all checks passed
if __name__ == "__main__":
    TEST_TERMS = ["badword1", "badword2"]
    
    
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
        check("contains_link ignores plain chat", contains_link("hey chat!"), False),
        # Permissions
        check("streamer can post links", can_post_links("@Reshir0m"), True),
        check("viewer can't post links", can_post_links("randomviewer"), False),
        # Decide action
        check("plain chat allowed", decide_action("hey chat what's up", "randomviewer"), "allow"),
        check("streamer link allowed", decide_action("www.example.com", "@Reshir0m"), "allow"),
        check("viewer link deleted", decide_action("FOLLOW ME www.example.com", "randomviewer"), "delete"),
        check("caps and spaces still caught", decide_action(  "WWW.EXAMPLE.COM  ", "randomviewer"), "delete"),
        check("twitch.tv without https", decide_action("check out twitch.tv/someone", "randomviewer"), "delete"),
        check("ok.come is not a link", decide_action("ok.come on chat", "randomviewer"), "allow"),
        check("link at end of sentence", decide_action("go to example.com.", "randomviewer"), "delete"),
        check("link before punctuation", decide_action("my stire is example.com!", "randomviewer"), "delete"),
        check("link shortener", decide_action("bit.ly/abc123", "randomviewer"), "delete"),
        check("punctuation isn't a link", decide_action("wait... really?", "randomviewer"), "allow"),
        # Decide action: blocklist
        check("blocked term bans", decide_action("you are a badword1", "randomviewer", TEST_TERMS), "ban"),
        check("blocked term caps + punctuation", decide_action("BADWORD1!", "randomviewer", TEST_TERMS), "ban"),
        check("ban beats delete", decide_action("badword1 www.example.com", "randomviewer", TEST_TERMS), "ban"),
        check("whole words only", decide_action("badword1x is fine", "randomviewer", TEST_TERMS), "allow"),
        check("contraction before term", decide_action("you're a badword1", "randomviewer", TEST_TERMS), "ban"),
        check("possessive on term", decide_action("that's badword1's fault", "randomviewer", TEST_TERMS), "ban"),
        check("curly apstrophe", decide_action("BADWORD1'S", "randomviewer", TEST_TERMS), "ban"),
        # any other asserts get converted the same way
    ]
    
    failed = results.count(False)
    if failed == 0:
        print("All checks passed!")
    else:
        print(f"{failed} check(s)")