def clean_username(name):
    """Return the username lowercased. with spaces removed"""
    name = name.strip()
    name = name.lower()
    if name.startswith("@"):
        name = name[1:]  # slice: everything from index 1 on, which drops the @
    return name


print(clean_username(" @Reshir0m ")) # should print reshir0m
print(clean_username("viewer123"))  # should print viewer123