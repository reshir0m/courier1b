def clean_username(name):
    """Return the username lowercase. with spaces removed"""
    name = name.strip()
    name = name.lower()
    if name.startswith("@"):
        name = name[1:]  # slice: everything from index 1 on, which drops the @
    return name



def normalize_text(text):
    """Return the message in lowercase, with spaces trimmed off both ends"""
    text = text.strip()
    text = text.lower()
    return text

print(clean_username(" @Reshir0m ")) # should print: reshir0m
print(clean_username("viewer123"))  # should print: viewer123
print(normalize_text("  WWW.EXAMPLE.COM  "))  # should print: www,example.com
print(normalize_text("@Reshi nice play!"))  # should print: @reshi nice play!