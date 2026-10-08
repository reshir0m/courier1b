import os
from dotenv import load_dotenv
from mssql_python import connect


# Configuration
load_dotenv()
CONN_STR = os.environ["COURIER1B_DB"]


# Blacklisted Configuration
def run_query(sql, params=()):
    """Run one query, save any changes, and return any rows produced"""
    conn = connect(CONN_STR)
    cursor = conn.cursor()
    cursor.execute(sql, params)
    rows = []
    if cursor.description:
        rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return rows



def load_blocked_terms():
    """Return every blocked term as a list of strings."""
    rows = run_query("SELECT term FROM blocked_terms")
    return [row[0] for row in rows]


def add_blocked_term(term, category):
    """Add one term to the blocklist unless it's already there."""
    term = term.strip().lower()
    run_query(
        "IF NOT EXISTS (SELECT 1 FROM blocked_terms WHERE term = ?) "
        "INSERT INTO blocked_terms (term, category) VALUES (?, ?)",
        (term, term, category),
    )


if __name__ == "__main__":
    print(load_blocked_terms())  # ['badword1']