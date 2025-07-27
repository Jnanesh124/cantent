import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import os
import json

# Load config from config.json or env
with open('config.json', 'r') as f:
    DATA = json.load(f)

def getenv(var):
    return os.environ.get(var) or DATA.get(var)

# Config values
bot_token = getenv("TOKEN")
api_hash = getenv("HASH")
api_id = int(getenv("ID"))
string_session = getenv("STRING")

# Help/Usage text
USAGE = """**FOR PUBLIC CHATS**

__Just send post(s) link__

**FOR PRIVATE CHATS**

__First send invite link of the chat, then send post(s) link__

**FOR BOT CHATS**

__Send link with `/b/`, bot's username and message ID__

**MULTI POSTS**

__Send links in format like "from - to" to send multiple messages__

__Spaces don’t matter__
"""

# Force-subscribe channels
REQUIRED_CHANNELS = ["@JN2FLIX", "@ROCKERSBACKUP"]

# Bot client
bot = Client(
    name="mybot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
    workdir="/tmp"
)

# Optional user session
if string_session:
    acc = Client(
        name="myacc",
        api_id=api_id,
        api_hash=api_hash,
        session_string=string_session,
        workdir="/tmp"
    )
    acc.start()
else:
    acc = None

# Check if user is member of required channels
async def is_user_member(user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except UserNotParticipant:
            return False
        except Exception as e:
            print(f"Error checking membership in {channel}: {e}")
            return False
    return True

# /start handler
@bot.on_message(filters.command(["start"]))
async def send_start(client, message):
    user_id = message.from_user.id
    if not await is_user_member(user_id):
        buttons = [
            [InlineKeyboardButton("Join Channel 1", url=f"https://t.me/{REQUIRED_CHANNELS[0][1:]}")],
            [InlineKeyboardButton("Join Channel 2", url=f"https://t.me/{REQUIRED_CHANNELS[1][1:]}")]
        ]
        await message.reply(
            "**You must join the required channels to use this bot. Once joined, press /start again.**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    await message.reply(
        f"**👋 Hi {message.from_user.mention}, I am Save Restricted Bot.**\n\n{USAGE}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Update Channel", url="https://t.me/ROCKERSBACKUP")]])
    )

# Main message handler
@bot.on_message(filters.text)
async def save(client, message):
    user_id = message.from_user.id
    if not await is_user_member(user_id):
        buttons = [
            [InlineKeyboardButton("Join Channel 1", url=f"https://t.me/{REQUIRED_CHANNELS[0][1:]}")],
            [InlineKeyboardButton("Join Channel 2", url=f"https://t.me/{REQUIRED_CHANNELS[1][1:]}")]
        ]
        await message.reply(
            "**You must join the required channels to use this bot. Once joined, press /start again.**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    print(message.text)

    # Handle join link
    if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:
        if acc is None:
            await message.reply("**String Session is not Set**")
            return

        try:
            await acc.join_chat(message.text)
            await message.reply("**Chat Joined**")
        except UserAlreadyParticipant:
            await message.reply("**Chat already Joined**")
        except InviteHashExpired:
            await message.reply("**Invalid Link**")
        except Exception as e:
            await message.reply(f"**Error:** {str(e)}")

# Start bot
bot.run()
