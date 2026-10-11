import os

import twitchio
from dotenv import load_dotenv
from twitchio import eventsub
from twitchio.ext import commands

from bot.commands import handle_command
from bot.db import load_blocked_terms
from bot.rules import decide_action, decide_automod, AUTO_APPROVE_CATEGORIES

ENABLE_BANS = True

load_dotenv()
CLIENT_ID = os.environ["TWITCH_CLIENT_ID"]
CLIENT_SECRET = os.environ["TWITCH_CLIENT_SECRET"]
BOT_ID = os.environ["BOT_ID"]
OWNER_ID = os.environ["OWNER_ID"]


def chat_subscription():
    """Listens in chat for an EventSub"""
    return eventsub.ChatMessageSubscription(broadcaster_user_id=OWNER_ID, user_id=BOT_ID)


def listen_automod():
    """Delivers every held Automod message in chat to bot."""
    return eventsub.AutomodMessageHoldV2Subscription(
        broadcaster_user_id=OWNER_ID,
        moderator_user_id=BOT_ID,
    )




class CourierBot(commands.AutoBot):
    def __init__(self):
        super().__init__(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            bot_id=BOT_ID,
            owner_id=OWNER_ID,
            prefix="!",
            subscriptions=[chat_subscription(), listen_automod()],
            force_subscribe=True,
        )
        self.blocked_terms = load_blocked_terms()
    
    async def event_oauth_authorized(self, payload):
        await self.add_token(payload.access_token, payload.refresh_token)
        if payload.user_id == OWNER_ID:
            await self.multi_subscribe([chat_subscription(), listen_automod()])
        
    async def event_ready(self):
        print("Bot is connected.")
    
    
    async def event_message(self, payload: twitchio.ChatMessage):
        """Runs for every chat message in channel."""
        if payload.chatter.id == BOT_ID:
            return
        print(f"{payload.chatter.name}: {payload.text}")
        
        if payload.chatter.id != OWNER_ID:
            action, reason = decide_action(payload.text, payload.chatter.name, self.blocked_terms)
            if action in ("ban", "delete"):
                await payload.delete(moderator=BOT_ID)
                if action == "ban" and ENABLE_BANS:
                    await payload.broadcaster.ban_user(
                        moderator=BOT_ID, user=payload.chatter.id, reason=reason,
                    )
                print(f"  -> {action}: {reason}")
                return
            
            reply = handle_command(payload.text, payload.chatter.name)
            if reply:
                await payload.broadcaster.send_message(sender=self.user, message=reply)
    
    async def event_automod_message_hold(self, payload: twitchio.AutomodMessageHold):
        """Runs every time Automod holds a message in chat"""
        print(f"Automod held {payload.user.name}: {payload.text} "
            f"(category={payload.category}, reason={payload.reason})")
        action, reason = decide_automod(payload.text, payload.category,
                                        self.blocked_terms, AUTO_APPROVE_CATEGORIES)
        moderator = self.create_partialuser(BOT_ID)
        
        if action == "deny_and_ban":
            await moderator.deny_automod_messages(payload.message_id)
            if ENABLE_BANS:
                await payload.broadcaster.ban_user(
                    moderator=BOT_ID, user=payload.user, reason=reason,
                )
        elif action == "approve":
            await moderator.approve_automod_messages(payload.message_id)
        print(f"  -> {action}: {reason}")
