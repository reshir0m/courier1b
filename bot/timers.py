from bot.commands import YOUTUBE_URL, DISCORD_URL

TIMER_INTERVAL = 600    # Every 10 minutes
MIN_CHAT_MESSAGES = 3

TIMER_MESSAGES = [
    f"Enjoying the stream? Come check out the YouTube channel: {YOUTUBE_URL}",
    f"Wanna talk to Reshi in between streams? Then come join the Discord: {DISCORD_URL}",
]


def next_timer_message(messages, index):
    """Return (message to post now, index to use next time)"""
    message = messages[index]
    next_index = (index + 1) % len(messages)
    return message, next_index



def should_post_timer(seconds_since_last, chat_since_last):
    """Return True if enough time has passed and chat has been active"""
    return seconds_since_last >= TIMER_INTERVAL and chat_since_last >= MIN_CHAT_MESSAGES
