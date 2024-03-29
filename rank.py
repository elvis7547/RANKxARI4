import asyncio
import random 
import os
import config
from config import MONGO_DB_URI
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant, PeerIdInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_USERNAME = os.environ.get("BOT_USERNAME", "ll_ts_security_ll_bot")
SUDO_USERS = list(map(int, os.environ.get("SUDO_USERS", "5957398316 6352061770").split()))
OWNER_ID = "6352061770"
LOG_ID = int(os.environ.get("LOGGER_ID", "-1001916618183"))
API_ID = "25450075"
API_HASH = "278e22b00d6dd565c837405eda49e6f2"
BOT_TOKEN = os.environ.get("BOT_TOKEN", "6759953581:AAHz1Tm4OL_-1K3WqlN2houHGWKjp1VDNEA")
IMAGE_URLS = [
    "https://telegra.ph/file/56f46a11100eb698563f1.jpg",
    "https://telegra.ph/file/66552cbeb49088f98f752.jpg",
    "https://telegra.ph/file/a9ada352fd34ec8a01013.jpg",
    "https://telegra.ph/file/47a852d5b1c4c11a497c2.jpg",
    "https://telegra.ph/file/f002db994f436aaee892c.jpg",
    "https://telegra.ph/file/35621d8878aefb0dcd899.jpg"
]


mongo_client = MongoClient(config.MONGO_DB_URI)
db = mongo_client["your_database_name"]
top_members_collection = db["top_members"]

user_data = {}

app = Client('my_bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def get_chat_member_safe(chat_id, user_id):
    try:
        chat_member = await app.get_chat_member(chat_id, user_id)
        return chat_member
    except UserNotParticipant:
        return None
    except PeerIdInvalid:
        return None

async def send_response(message, response, reply_markup=None):
    await message.reply_text(response, reply_markup=reply_markup)

@app.on_message(filters.command("ranking"))
async def top_members(_, message):
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🍃ᴛᴏᴅᴀʏ🍃", callback_data="today"),
                InlineKeyboardButton("🍃ᴛᴏᴛᴀʟ🍃", callback_data="total")
            ],
            [
                InlineKeyboardButton("🍃ᴄʜᴀɴɴᴇʟ🍃", callback_data="channel"),
                InlineKeyboardButton("🍃ɢʀᴏᴜᴘ🍃", callback_data="group")
            ]
        ]
    )

    await send_response(message, "❀｡:•.─────  ❁ - ❁  ─────.•:｡❀\n ❤️‍🔥<b>ᴡᴇʟᴄᴏᴍᴇ, ᴛʜɪꜱ ʙᴏᴛ ᴡɪʟʟ ᴄᴏᴜɴᴛ ɢʀᴏᴜᴘ ᴍᴇꜱꜱᴀɢᴇꜱ\n ᴄʀᴇᴀᴛᴇ ʀᴀɴᴋɪɴɢꜱ ᴀɴᴅ ɢɪᴠᴇ ᴘʀɪᴢᴇꜱ ᴛᴏ ᴜꜱᴇʀꜱ!\n ᴍᴀᴅᴇ ᴡɪᴛʜ ❤️‍🔥ʙʏ ||ᴀʀɪ||❣️ \n❀｡:•.─────  ❁ - ❁  ─────.•:｡❀", reply_markup)

@app.on_callback_query()
async def callback_handler(_, query):
    if query.data == "today":
        await handle_today_query(query)
    elif query.data == "total":
        await handle_total_query(query)
    elif query.data == "channel":
        await handle_channel_query(query)
    elif query.data == "group":
        await handle_group_query(query)

async def handle_today_query(query):
    top_members = get_top_members("today")
    response = " 𝗧𝗢𝗗𝗔𝗬 𝗟𝗘𝗔𝗗𝗘𝗥𝗕𝗢𝗔𝗥𝗗:\n\n"
    counter = 1
    for member in top_members:
        user_id = member["_id"]
        chat_member = await get_chat_member_safe(query.message.chat.id, user_id)
        
        if chat_member:
            total_messages = member["total_messages"]
            full_name = f"{chat_member.user.first_name} {chat_member.user.last_name}" if chat_member.user.last_name else chat_member.user.first_name
            username = chat_member.user.username
            user_info = f"{counter}. {full_name} , ⏤͟͞{total_messages}\n"
            
            response += user_info
            counter += 1

    await query.message.edit_text(response)

async def handle_total_query(query):
    top_members = get_top_members("overall")
    response = " 𝗚𝗟𝗢𝗕𝗔𝗟 𝗟𝗘𝗔𝗗𝗘𝗥𝗕𝗢𝗔𝗥𝗗 | 🌍\n\n"
    counter = 1
    for member in top_members:
        user_id = member["_id"]
        chat_member = await get_chat_member_safe(query.message.chat.id, user_id)
        
        if chat_member:
            total_messages = member["total_messages"]
            full_name = f"{chat_member.user.first_name} {chat_member.user.last_name}" if chat_member.user.last_name else chat_member.user.first_name
            username = chat_member.user.username
            user_info = f"{counter}. {full_name}, ⏤͟͞{total_messages}\n"
            
            response += user_info
            counter += 1

    await query.message.edit_text(response)

async def handle_channel_query(query):
    await query.message.reply_text("𝗝𝗼𝗶𝗻 𝗼𝘂𝗿 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝗳𝗼𝗿 𝗺𝗼𝗿𝗲 𝘂𝗽𝗱𝗮𝘁𝗲𝘀: @ll_about_ari_ll")

async def handle_group_query(query):
    await query.message.reply_text("𝗝𝗼𝗶𝗻 𝗼𝘂𝗿 𝗴𝗿𝗼𝘂𝗽 𝗳𝗼𝗿 𝗱𝗶𝘀𝗰𝘂𝘀𝘀𝗶𝗼𝗻𝘀: @three_stars_ki_duniya")

def get_top_members(timeframe):
    if timeframe == "overall":
        return top_members_collection.find().sort("total_messages", -1).limit(10)
    elif timeframe == "today":
        today_start = datetime.combine(datetime.today(), datetime.min.time())
        today_end = today_start + timedelta(days=1)
        return top_members_collection.find({
            "last_updated": {"$gte": today_start, "$lt": today_end}
        }).sort("total_messages", -1).limit(10)

@app.on_message()
async def handle_messages(_, message):
    user_id = message.from_user.id
    user_data.setdefault(user_id, {}).setdefault("total_messages", 0)
    user_data[user_id]["total_messages"] += 1

    today_start = datetime.combine(datetime.today(), datetime.min.time())
    top_members_collection.update_one(
        {"_id": user_id},
        {"$inc": {"total_messages": 1}, "$set": {"last_updated": datetime.now()}},
        upsert=True
    )

@app.on_message(filters.private & filters.command("start"))
async def start_private_chat(client, message):
    # Choose a random image URL
    image_url = random.choice(IMAGE_URLS)

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("❤️‍🔥ᴀᴅᴅ ᴍᴇ❤️‍🔥", url=f"t.me/{BOT_USERNAME}?startgroup=true"),
                InlineKeyboardButton("💫ꜱᴜᴘᴘᴏʀᴛ💫", url=f"t.me/{SUPPORT_GROUP_USERNAME}"),
            ],
            [
                InlineKeyboardButton("💖ꜱᴏᴜʀᴄᴇ💖", url=f"t.me/{SOURCE_CODE_CHANNEL_USERNAME}"),
            ]
        ]
    )

    await client.send_photo(
        chat_id=message.chat.id,
        photo=image_url,
        caption="<b>нυι</b> тнιѕ ιѕ 「🛡ᴛꜱ ʀᴀɴᴋɪɴɢ ʙᴏᴛ🛡」❖ 💖\n"
                "♡━━━━━━━━ ᴀʀɪ ━━━━━━━♡\n"
                "💫 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛꜱ ʀᴀɴᴋɪɴɢ ʙᴏᴛ!.\n "
                "🌟 ᴅɪꜱᴄᴏᴠᴇʀ ᴡʜᴏ ꜱʜɪɴᴇꜱ ᴛʜᴇ ʙʀɪɢʜᴛᴇꜱᴛ ɪɴ ᴏᴜʀ ᴄᴏᴍᴍᴜɴɪᴛʏ! ꜰʀᴏᴍ ᴀᴄᴛɪᴠᴇ ᴍᴇᴍʙᴇʀꜱ ᴛᴏ ᴛᴏᴘ ᴄᴏɴᴛʀɪʙᴜᴛᴏʀꜱ, ᴡᴇ'ʀᴇ ʜᴇʀᴇ ᴛᴏ ʀᴇᴄᴏɢɴɪᴢᴇ ᴇxᴄᴇʟʟᴇɴᴄᴇ.\n"
                "📊 Stay updated with real-time rankings, track your progress, and compete with friends to climb the leaderboard!\n"
                "❖Join us in celebrating achievements and fostering a vibrant community together!❖\n"
                "♡━━━━━━━━ ᴀʀɪ ━━━━━━━♡\n\n"
                "ᴍᴀᴅᴇ ᴡɪᴛʜ 🖤 ʙʏ <a href=\"https://t.me/lll_notookk_lll\">||ᴀʀɪ||❣️</a>",
        reply_markup=keyboard
    )
    accha = await message.reply_text(
        text="__ᴅιиg ᴅιиg ꨄ︎ ѕтαятιиg..__"
    )
    await asyncio.sleep(0.2)
    await accha.edit("__ᴅιиg ᴅιиg ꨄ sтαятιиg.....__")
    await asyncio.sleep(0.2)
    await accha.edit("__ᴅιиg ᴅιиg ꨄ︎ sтαятιиg..__")
    await asyncio.sleep(0.2)
    await accha.delete()

app.run()
