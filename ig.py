import telebot
import threading
import time 
import logging
import re
import os
import requests
from instaloader import Instaloader, Post
from telebot import types
import subprocess
import yt_dlp
from bs4 import BeautifulSoup
import json

# Logging setup
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot Token
TOKEN = "8056603811:AAH32j_hunSJEHTzwaFzB1b8rbybVlVbzWg"  # Set this in your environment variables

bot = telebot.TeleBot(TOKEN)

# Instagram credentials (set in environment variables)
user_ids = []

ADMIN_ID = "7858368373"
channel_ids = []
OWNER_ID = '7858368373'


# Dictionary to store users and their downloads
user_downloads = {}

def is_admin(chat_id, user_id):
    try:
        chat_admins = bot.get_chat_administrators(chat_id)
        return any(admin.user.id == user_id for admin in chat_admins)
    except Exception as e:
        return False
        
# Load user IDs from file
def load_user_ids():
    global user_ids
    if os.path.exists("user_ids.txt"):
        with open("user_ids.txt", "r") as f:
            user_ids = [int(line.strip()) for line in f.readlines()]

def load_channel_ids():
    global channel_ids
    if os.path.exists("channel_ids.txt"):
        with open("channel_ids.txt", "r") as f:
            channel_ids = [int(line.strip()) for line in f.readlines()]
            
            
# Save user IDs to file
def save_user_ids():
    with open("user_ids.txt", "w") as f:
        for user_id in user_ids:
            f.write(f"{user_id}\n")

def save_channel_ids():
    with open("channel_ids.txt", "w") as f:
        for channel_id in channel_ids:
            f.write(f"{channel_id}\n")
            

#_&________

def get_moj_video(moj_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(moj_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # First try OpenGraph Meta Tag
        meta_tag = soup.find("meta", property="og:video")
        if meta_tag and meta_tag["content"]:
            return meta_tag["content"]

        # Try JSON Extraction
        return extract_moj_video_from_json(response.text)
    
    return None

def extract_moj_video_from_json(html_content):
    pattern = r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});'
    match = re.search(pattern, html_content, re.DOTALL)
    
    if match:
        json_data = json.loads(match.group(1))
        try:
            return json_data["videoData"]["videoUrl"]
        except KeyError:
            return None
    return None
#_____&&
@bot.message_handler(func=lambda message: message.text and "https://mojapp.in/" in message.text)
def download_moj_video(message):
    video_url = get_moj_video(message.text)
    
    if video_url:
        bot.send_video(message.chat.id, video_url, caption="⦿ 🎥 𝐇𝐞𝐫𝐞 𝐢𝐬 𝐲𝐨𝐮𝐫 𝐌𝐨𝐣 𝐯𝐢𝐝𝐞𝐨 🪅\n\n\n☢ 𝙞𝙣𝙨𝙜𝙧𝙖𝙢 𝙧𝙚𝙚𝙡 𝙙𝙤𝙬𝙣𝙡𝙤𝙖𝙙 𝙗𝙤𝙩 🔸 @Dbdjdjdjdjdjbot ☢")
    else:
        bot.send_message(message.chat.id, "⚠̶️̶ ̶U̶n̶a̶b̶l̶e̶ ̶t̶o̶ ̶f̶e̶t̶c̶h̶ ̶t̶h̶e̶ ̶v̶i̶d̶e̶o̶.̶ ̶T̶r̶y̶ ̶a̶g̶a̶i̶n")
        
#₹________
def download_audio(instagram_url):
    try:
        ydl_opts = {
            'format': 'bestaudio/bbest',
            'outtmpl': 'BYE-@MR_ARMAN_OWNER.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([instagram_url])

        return "BYE-@MR_ARMAN_OWNER.mp3"
    
    except Exception as e:
        return None

import telebot
import instaloader
import os
import ffmpeg 


loader = instaloader.Instaloader()

# /story Command - Download Instagram Story
@bot.message_handler(commands=['story'])
def download_story(message):
    chat_id = message.chat.id
    args = message.text.split(" ")

    if len(args) < 2:
        bot.send_message(chat_id, "❌ **Usage:** `/story <Instagram Username>`", parse_mode="Markdown")
        return

    username = args[1].strip()

    bot.send_message(chat_id, "📥 **Fetching Instagram Story...**")

    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        for story in loader.get_story_items(profile.userid):
            story_url = story.video_url if story.is_video else story.url
            bot.send_message(chat_id, "📸 **Instagram Story:**")
            bot.send_video(chat_id, story_url) if story.is_video else bot.send_photo(chat_id, story_url)

        bot.send_message(ADMIN_ID, f"📥 **New Story Download**\n👤 User: `{chat_id}`\n🔗 Username: `{username}`", parse_mode="Markdown")

    except Exception as e:
        bot.send_message(chat_id, f"❌ `{str(e)}`", parse_mode="Markdown")

# /post Command - Download Instagram Post (Photo, Video, Carousel)
@bot.message_handler(commands=['post'])
def download_post(message):
    chat_id = message.chat.id
    args = message.text.split(" ")

    if len(args) < 2:
        bot.send_message(chat_id, "❌ **Usage:** `/post <Instagram Link>`", parse_mode="Markdown")
        return

    ig_link = args[1].strip()

    bot.send_message(chat_id, "📥 Fetching Instagram Post...")

    try:
        post = instaloader.Post.from_shortcode(loader.context, ig_link.split("/")[-2])
        caption_text = post.caption[:1000] if post.caption else "No caption available."
        
        # If post contains multiple photos/videos
        media_list = []
        if post.typename == "GraphSidecar":  # Multiple images/videos
            for item in post.get_sidecar_nodes():
                media_list.append(item.video_url if item.is_video else item.display_url)
        else:
            media_list.append(post.video_url if post.is_video else post.url)

        # Send all media
        for media in media_list:
            bot.send_video(chat_id, media) if media.endswith(".mp4") else bot.send_photo(chat_id, media)

        # Send Caption
        bot.send_message(chat_id, f"📄 **Caption:**\n\n{caption_text}")

        bot.send_message(ADMIN_ID, f"📥 **New Post Download**\n👤 User: `{chat_id}`\n🔗 Link: {ig_link}", parse_mode="Markdown")

    except Exception as e:
        bot.send_message(chat_id, f"❌ `{str(e)}`", parse_mode="Markdown")

# /audio Command - Convert IG Video to MP3
@bot.message_handler(commands=['audio'])
def download_audio(message):
    chat_id = message.chat.id
    args = message.text.split(" ")
    
    if len(args) < 2:
        bot.send_message(chat_id, "❌ **Usage:** `/audio <Instagram Link>`", parse_mode="Markdown")
        return
    
    ig_link = args[1].strip()

    bot.send_message(chat_id, "🎵 Extracting audio from Instagram video...")
    
    try:
        post = instaloader.Post.from_shortcode(loader.context, ig_link.split("/")[-2])
        video_url = post.video_url
        temp_video = "temp_video.mp4"
        temp_audio = "temp_audio.mp3"

        # Download Video File
        os.system(f'wget "{video_url}" -O {temp_video}')

        # Convert Video to MP3
        ffmpeg.input(temp_video).output(temp_audio, format="mp3", audio_bitrate="128k").run(overwrite_output=True)

        # Send Audio
        bot.send_audio(chat_id, open(temp_audio, "rb"), title="Instagram Reel Audio")

        # Delete Temp Files
        os.remove(temp_video)
        os.remove(temp_audio)

        # Notify Admin
        bot.send_message(ADMIN_ID, f"🎵 **New Audio Download**\n👤 User: `{chat_id}`\n🔗 Link: {ig_link}", parse_mode="Markdown")

    except Exception as e:
        bot.send_message(chat_id, "❌ **Failed to extract audio.**\nMaybe the link is private or incorrect.")
        bot.send_message(ADMIN_ID, f"⚠️ **Audio Download Failed** for {chat_id}\nError: {str(e)}")


@bot.message_handler(func=lambda message: "https://www.instagram.com/reel/" in message.text.lower())
def download_instagram_video(message):
    chat_id = message.chat.id
    ig_link = message.text.strip()

    # Delete user's message for privacy
    try:
        bot.delete_message(chat_id, message.message_id)
    except:
        pass  # If unable to delete, continue

    bot.send_message(chat_id, "⏳ Downloading your Instagram video...")
    
    try:
        post = instaloader.Post.from_shortcode(loader.context, ig_link.split("/")[-2])
        video_url = post.video_url
        caption_text = post.caption[:1000] if post.caption else "No caption available."

        # Send video
        bot.send_video(chat_id, video_url, caption="✅ Download Complete!")

        # Send caption separately
        bot.send_message(chat_id, f"{caption_text}")

        # Notify Admin
        bot.send_message(ADMIN_ID, f"📥 **New Download**\n👤 User: `{chat_id}`\n🔗 Link: {ig_link}")

    except Exception as e:
        bot.send_message(chat_id, "❌ **Failed to download video.**\nMaybe the link is private or incorrect.")
        bot.send_message(ADMIN_ID, f"⚠️ **Download Failed** for {chat_id}\nError: {str(e)}")




from telebot import types


@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    user_name = message.from_user.username or "No Username"
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "Unknown"

    # Step 1: Check if the user is new and save their ID
    if user_id not in user_ids:
        user_ids.append(user_id)
        save_user_ids()

    # Step 2: Send a temporary loading message
    temp_msg = bot.send_message(chat_id, "⌛")
    time.sleep(2)
    bot.delete_message(chat_id, temp_msg.message_id)

    # Step 3: Show typing animation
    bot.send_chat_action(chat_id, "typing")
    time.sleep(0.5)  # Simulate typing delay

    # Step 4: Prepare welcome message
    caption_text = (
        f"👋 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ɪɴsᴛᴀɢʀᴀᴍ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ʙᴏᴛ\n\n"
        f"⦿ 🆔 𝚈𝙾𝚄𝚁 𝙽𝙰𝙼𝙴 - @{user_name}\n"
        f"⦿ 🆔 𝚈𝙾𝚄𝚁 𝙸𝙳 - {user_id}\n"
        f"⦿ 🆔 𝚈𝙾𝚄𝚁 𝙵𝙸𝚁𝚂𝚃 𝙽𝙰𝙼𝙴 - {first_name}\n\n"
        "📩 𝐒𝐞𝐧𝐝 𝐦𝐞 𝐚𝐧𝐲 𝐩𝐮𝐛𝐥𝐢𝐜 𝐈𝐧𝐬𝐭𝐚𝐠𝐫𝐚𝐦 𝐥𝐢𝐧𝐤 (𝐑𝐞𝐞𝐥𝐬, 𝐏𝐨𝐬𝐭𝐬, 𝐞𝐭𝐜.), 𝐚𝐧𝐝 𝐈'𝐥𝐥 𝐡𝐞𝐥𝐩 𝐲𝐨𝐮 𝐝𝐨𝐰𝐧𝐨𝐚𝐝 𝐢𝐭\n\n"
        "/post <url> to download post\n"
        "/audio <url> to download audio"
        "GUVE ME ANY REEL URL TO DOWNLOAD"
    )

    # Step 5: Create Inline Keyboard with Buttons
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("➕ ᴬᵈᵈ ᴹᵉ ᵗᵒ ʸᵒᵘʳ ᴳʳᵒᵘᵖ", url=f"https://t.me/{bot.get_me().username}?startgroup=true"))
    keyboard.add(types.InlineKeyboardButton("📢 J‌‌  O‌‌  I‌‌  N‌‌  ", url="https://t.me/ARMANTEAMVIP"))
    keyboard.add(types.InlineKeyboardButton("👨‍💻 𝙳𝙴𝚅𝙴𝙻𝙾𝙿𝙴𝚁", url="https://t.me/MR_ARMAN_OWNER"))

    # Step 6: Fetch user's profile photo (if available)
    photos = bot.get_user_profile_photos(user_id)
    if photos.total_count > 0:
        # Get the highest resolution photo
        photo = photos.photos[0][-1].file_id
        bot.send_photo(chat_id, photo, caption=caption_text, parse_mode="Markdown", reply_markup=keyboard)
    else:
        bot.send_message(chat_id, caption_text, parse_mode="Markdown", reply_markup=keyboard)

def get_user_ids():
    with open("user_ids.txt", "r") as file:
        return file.readlines()

# Command for broadcasting
@bot.message_handler(commands=['broadcast'])
def handle_broadcast(message):
    if str(message.from_user.id) == OWNER_ID:
        bot.send_message(message.chat.id, "Please send the broadcast message or a photo with a caption (if no caption, just send the photo).")
        bot.register_next_step_handler(message, process_broadcast)
    else:
        bot.send_message(message.chat.id, "You are not authorized.")

def process_broadcast(message):
    user_ids = get_user_ids()
    
    if message.content_type == 'text':
        # Send text broadcast
        text = message.text
        for user_id in user_ids:
            try:
                bot.send_message(user_id.strip(), text)
            except Exception as e:
                print(f"Failed to send to {user_id.strip()}: {e}")
    elif message.content_type == 'photo':
        # Send photo broadcast
        caption = message.caption if message.caption else None
        photo = message.photo[-1].file_id  # Get the highest quality photo
        for user_id in user_ids:
            try:
                bot.send_photo(user_id.strip(), photo, caption=caption)
            except Exception as e:
                print(f"Failed to send to {user_id.strip()}: {e}")

@bot.message_handler(commands=["help"])
def help(message):
    chat_id = message.chat.id
    user_name = message.from_user.username if message.from_user.username else "No Username"
    first_name = message.from_user.first_name if message.from_user.first_name else "Unknown"

    help_text = (
        f"👋  {first_name}! 𝙷𝚎𝚕𝚕𝚘 𝙷𝚎𝚛𝚎'𝚜 𝚑𝚘𝚠 𝙸 𝚌𝚊𝚗 𝚊𝚜𝚜𝚒𝚜𝚝 𝚢𝚘𝚞🔹\n\n"
        f"⦿ 𝐔𝐬𝐞 /𝐚𝐮𝐝𝐢𝐨 <𝐫𝐞𝐞𝐥_𝐮𝐫𝐥> 𝐭𝐨 𝐝𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐚𝐮𝐝𝐢𝐨 𝐟𝐫𝐨𝐦 𝐚 𝐯𝐢𝐝𝐞𝐨.🔹\n\n"
        f"⦿ 𝐝𝐢𝐫𝐞𝐜𝐭 𝐥𝐢𝐧𝐤 𝐝𝐚𝐚𝐥𝐨 𝐯𝐢𝐝𝐞𝐨 𝐯𝐢𝐝𝐞𝐨 𝐦𝐢𝐥 𝐣𝐚𝐲𝐞𝐠𝐚 𝐭𝐡𝐮𝐦𝐞🔹\n\n"
        f"⦿ 𝙶𝙸𝚅𝙴 𝙼𝙴 𝙰𝙽𝚈 𝙼𝙾𝙹 𝚅𝙸𝙳𝙴𝙾 𝚄𝚁𝙻 𝙰𝙽𝙳 𝙸'𝙻𝙻 𝙸𝙼𝙼𝙴𝙳𝙸𝙰𝚃𝙴𝙻𝚈 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳 𝙰𝙽𝙳 𝚂𝙴𝙽𝙳 𝚈𝙾𝚄🔹\n\n"
        f"⦿ 𝙁𝙤𝙧 𝙖𝙣𝙮 𝙛𝙪𝙧𝙩𝙝𝙚𝙧 𝙦𝙪𝙚𝙨𝙩𝙞𝙤𝙣𝙨 𝙤𝙧 𝙛𝙚𝙚𝙙𝙗𝙖𝙘𝙠, 𝙛𝙚𝙚𝙡 𝙛𝙧𝙚𝙚 𝙩𝙤 𝙧𝙚𝙖𝙘𝙝 𝙤𝙪𝙩!"
    )

    # Send the help message
    bot.send_message(chat_id, help_text)
    
    
# Command: Users (Admin only)
@bot.message_handler(commands=["users"])
def list_users(message):
    if str(message.chat.id) != ADMIN_ID:
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return
    
    if not user_downloads:
        bot.reply_to(message, "📂 No user data available.")
        return

    users_text = "📜 User Download List:\n\n"
    for user_id, details in user_downloads.items():
        users_text += f"👤 Username: {details['username']}\n"
        users_text += f"🆔 User ID: {user_id}\n"
        users_text += f"📥 Downloaded Videos: {len(details['downloads'])}\n"
        users_text += "_________________________\n"

    bot.send_message(message.chat.id, users_text)


# Support command handler
@bot.message_handler(commands=['support'])
def support_command(message):
    bot.reply_to(message, "📞 𝙵𝚘𝚛 𝚜𝚞𝚙𝚙𝚘𝚛𝚝, 𝚙𝚕𝚎𝚊𝚜𝚎 𝚌𝚘𝚗𝚝𝚊𝚌𝚝 @MR_ARMAN_OWNER 𝚘𝚛 𝚟𝚒𝚜𝚒𝚝 𝚘𝚞𝚛 𝚜𝚞𝚙𝚙𝚘𝚛𝚝 𝚐𝚛𝚘𝚞𝚙 : @ARMANTEAMVIP")

# Handle Video and Process in a separate thread to speed up
def process_video(message, video_file_id):
    video = bot.get_file(video_file_id)
    video_file_path = f'{video_file_id}.mp4'

    try:
        downloaded_file = bot.download_file(video.file_path)
        with open(video_file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "⦿ 🔄 ᴘʀᴏᴄᴇᴤᴤɪɴɢ ʏᴏᴜʀ ᴠɪᴅᴇᴏ, ᴘʟᴇᴀᴤᴇ ᴡᴀɪᴛ...🔹")

        if os.path.getsize(video_file_path) > 18 * 1024 * 1024:
            bot.reply_to(message, "❌ 𝙎𝙤𝙧𝙧𝙮, 𝙩𝙝𝙚 𝙫𝙞𝙙𝙚𝙤 𝙨𝙞𝙯𝙚 𝙚𝙭𝙘𝙚𝙚𝙙𝙨 18𝙈𝘽.")
            os.remove(video_file_path)
            return

        audio_file_path = f'{video_file_id}.mp3'
        command = f'ffmpeg -i "{video_file_path}" -q:a 0 -map a "{audio_file_path}" -threads 4 -preset fast'
        subprocess.run(command, shell=True)

        bot.send_chat_action(message.chat.id, 'upload_audio')
        with open(audio_file_path, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, caption="⦿ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏᴇ : @Sidgkdigdjgzigdotxotbot🔹")

        os.remove(video_file_path)
        os.remove(audio_file_path)

        bot.send_message(message.chat.id, "👉 ⦿ 𝙿𝙻𝙴𝙰𝚂𝙴 𝙹𝙾𝙸𝙽 : @ARMANTEAMVIP🔹")

    except Exception as e:
        bot.reply_to(message, "̶⚠̶️̶ ̶A̶n̶ ̶e̶r̶r̶o̶r̶ ̶o̶c̶c̶u̶r̶r̶e̶d̶ ̶d̶u̶r̶i̶n̶g̶ ̶p̶r̶o̶c̶e̶s̶s̶i̶n̶g̶.̶ ̶P̶l̶e̶a̶s̶e̶ ̶t̶r̶y̶ ̶a̶g̶a̶i̶n̶ ̶l̶a̶t̶e̶r̶.")
        print(f"Error: {e}")



import os
import asyncio
import datetime
import aiofiles
from random import choice
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import *
from database import Database

# 🔹 Define Config Variables (Previously in config.py)

API_ID = 27152769  # Replace with your actual API ID
API_HASH = "b98dff566803b43b3c3120eec537fc1d"
DATABASE_URL = "mongodb://user1:abhinai.2244@cluster0.7oaqx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# 🔹 Database Setup
db = Database(DATABASE_URL, "autoreactionbot")

# 🔹 List of Emojis for Reactions
EMOJIS = [
    "👍", "❤", "🔥", "🥰", "😁", "🤔", "🤯", "😱", "🤬", 
    "🥶", "🤩", "🥳", "😎", "🙏", "🤣", "😇", "🥱",  "😍", 
    "❤‍🔥", "🌚", "😐", "💯", "🦄", "⚡", "👾", "🏆", "💔", "🤨", "😡", 
    "😘", "😈", "😴", "😭", "👻", "👀", "🎃", "🙄", 
    "😨", "🤝", "🤐", "🤗", "🤭", "🤫", "🤪", "😏"
]


# 🔹 Bot Setup
Bot = Client(
    "Dbdjdjdjdjdjbot",
    bot_token=TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
)

@Bot.on_message(filters.group | filters.private)  # 👈 Group + DM me reaction
async def send_reaction(_, msg: Message):
    try:
        await msg.react(choice(EMOJIS))
    except Exception as e:
        print(f"Error reacting to message: {e}")  


def run_telebot():
    print("🤖 Telebot Started!")
    bot.infinity_polling()


def run_pyrogram():
    print("🚀 Pyrogram Bot Started!")
    asyncio.run(pyro_bot.run())


# ✅ **Start Both Bots in Separate Threads**
if __name__ == "__main__":
    threading.Thread(target=run_telebot).start()
    Bot.run()