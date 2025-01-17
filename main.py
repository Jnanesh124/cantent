import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import os
import threading
import json

# Load configuration
with open('config.json', 'r') as f:
    DATA = json.load(f)

def getenv(var):
    return os.environ.get(var) or DATA.get(var, None)

# Initialize bot and account
bot_token = getenv("TOKEN")
api_hash = getenv("HASH")
api_id = getenv("ID")
bot = Client("mybot", api_id=api_id, api_hash=api_id, bot_token=bot_token)

ss = getenv("STRING")
if ss is not None:
    acc = Client("myacc", api_id=api_id, api_hash=api_hash, session_string=ss)
    acc.start()
else:
    acc = None

# Required channels for force subscribe
REQUIRED_CHANNELS = ["@JN2FLIX", "@ROCKERSBACKUP"]

# Function to check user membership in channels
async def is_user_member(user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status in ["member", "administrator", "creator"]:
                continue
            else:
                return False
        except UserNotParticipant:
            return False
        except Exception as e:
            print(f"Error checking membership in {channel}: {e}")
            return False
    return True

# Start command
@bot.on_message(filters.command(["start"]))
async def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    user_id = message.from_user.id
    if not await is_user_member(user_id):
        buttons = [[InlineKeyboardButton("Join Channel 1", url=f"https://t.me/{REQUIRED_CHANNELS[0][1:]}")],
                   [InlineKeyboardButton("Join Channel 2", url=f"https://t.me/{REQUIRED_CHANNELS[1][1:]}")]]
        await bot.send_message(
            message.chat.id,
            "**You must join the required channels to use this bot. Once joined, press /start again.**",
            reply_markup=InlineKeyboardMarkup(buttons),
            reply_to_message_id=message.id
        )
        return

    await bot.send_message(
        message.chat.id,
        f"**__👋 Hi** **{message.from_user.mention}**, **I am Save Restricted Bot, I can send you restricted content by its post link__**\n\n{USAGE}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Update Channel", url="https://t.me/ROCKERSBACKUP")]]),
        reply_to_message_id=message.id
    )

# Handler for text messages with force-subscribe check
@bot.on_message(filters.text)
async def save(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    user_id = message.from_user.id
    if not await is_user_member(user_id):
        buttons = [[InlineKeyboardButton("Join Channel 1", url=f"https://t.me/{REQUIRED_CHANNELS[0][1:]}")],
                   [InlineKeyboardButton("Join Channel 2", url=f"https://t.me/{REQUIRED_CHANNELS[1][1:]}")]]
        await bot.send_message(
            message.chat.id,
            "**You must join the required channels to use this bot. Once joined, press /start again.**",
            reply_markup=InlineKeyboardMarkup(buttons),
            reply_to_message_id=message.id
        )
        return

    # Existing message handling logic
    print(message.text)

    # Joining chats
    if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:
        if acc is None:
            await bot.send_message(message.chat.id, f"**String Session is not Set**", reply_to_message_id=message.id)
            return

        try:
            await acc.join_chat(message.text)
            await bot.send_message(message.chat.id, "**Chat Joined**", reply_to_message_id=message.id)
        except UserAlreadyParticipant:
            await bot.send_message(message.chat.id, "**Chat already Joined**", reply_to_message_id=message.id)
        except InviteHashExpired:
            await bot.send_message(message.chat.id, "**Invalid Link**", reply_to_message_id=message.id)

    # Getting message logic (unchanged from your original code)

# Other supporting functions like `handle_private`, `downstatus`, `upstatus`, etc., remain unchanged.

USAGE = """**FOR PUBLIC CHATS**

**__just send post/s link__**

**FOR PRIVATE CHATS**

**__first send invite link of the chat (unnecessary if the account of string session already member of the chat) then send post/s link__**

**FOR BOT CHATS**

**__send link with** '/b/', **bot's username and message id, you might want to install some unofficial client to get the id like below__**


**MULTI POSTS**

**__send public/private posts link as explained above with format "from - to" to send multiple messages like below__**


**__note that space in between doesn't matter__**
"""

# Infinity polling
bot.run()
