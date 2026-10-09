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
    """Return (action, reason) for chat message. No side effects."""
    cleaned = normalize_text(text)
    if contains_blocked_term(cleaned, blocked_terms):
        return "ban", "used a blocked term"
    if contains_link(cleaned) and not can_post_links(username):
        return "delete", "posted a link without permission"
    return "allow", ""

def carry_out(action, username, reason):
    """Acts on verdict. The only function with side effects."""
    if action == "ban":
        print(f"Banned {username}: {reason}")
    elif action == "delete":
        print(f"Deleted a message from {username}: {reason}")


# Only prints if all checks passed