import os

import twitchio
from dotenv import load_dotenv
from twitchio import eventsub
from twitchio.ext import commands

from bot.commands import handle_command


load_dotenv()
CLIENT_ID = os.environ["TWITCH_CLIENT_ID"]
CLIENT_SECRET = os.environ["TWITCH_CLIENT_SECRET"]
BOT_ID = os.environ["BOT_ID"]
OWNER_ID = os.environ["OWNER_ID"]


def chat_subscription():
    """Listens in chat for an EventSub"""
    return eventsub.ChatMessageSubscription(broadcaster_user_id=OWNER_ID, user_id=BOT_ID)


class CourierBot(commands.AutoBot):
    def __init__(self):
        super().__init__(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            bot_id=BOT_ID,
            owner_id=OWNER_ID,
            prefix="!",
            subscriptions=[chat_subscription()],
            force_subscribe=True,
        )
    
    async def event_oauth_authorized(self, payload):
        await self.add_token(payload.access_token, payload.refresh_token)
        if payload.user_id == OWNER_ID:
            await self.multi_subscribe([chat_subscription()])
        
    async def event_ready(self):
        print("Bot is connected.")
    
    
    async def event_message(self, payload: twitchio.ChatMessage):
        """Runs for every chat message in channel."""
        if payload.chatter.id == BOT_ID:
            return
        print(f"{payload.chatter.name}: {payload.text}")
        reply = handle_command(payload.text, payload.chatter.name)
        if reply:
            await payload.broadcaster.send_message(sender=self.user, message=reply)
