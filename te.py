import telebot
import os
import time
import gtts
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
from telebot import types

# Bot Token
BOT_TOKEN = "7729803490:AAGPlYiqOqa99--WxnNBjySyIoC-W29ahZs"
bot = telebot.TeleBot(BOT_TOKEN)

# Temporary storage path for audio files
AUDIO_PATH = "tts_audio"

# Ensure the folder exists
os.makedirs(AUDIO_PATH, exist_ok=True)


ADMIN_ID = 7858368373

repeat_cache = {}
processing_messages = {}
banned_users = set()
user_data = {}


@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.chat.id == ADMIN_ID:
        try:
            user_id = int(message.text.split()[1])
            banned_users.add(user_id)
            bot.send_message(user_id, "🚫 ʏou нᴀvᴇ ʙᴇᴇɴ *ʙᴀɴɴᴇᴅ* ғʀoм usιɴԍ тнιs ʙoт.", parse_mode="Markdown")
            bot.send_message(ADMIN_ID, f"✅ User {user_id} has been *banned*.")
        except:
            bot.send_message(ADMIN_ID, "⚠️ Invalid command. Use: `/ban <user_id>`", parse_mode="Markdown")

@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.chat.id == ADMIN_ID:
        try:
            user_id = int(message.text.split()[1])
            if user_id in banned_users:
                banned_users.remove(user_id)
                bot.send_message(user_id, "✅ You have been *unbanned*.", parse_mode="Markdown")
                bot.send_message(ADMIN_ID, f"✅ User {user_id} has been *unbanned*.")
            else:
                bot.send_message(ADMIN_ID, "⚠️ User is not banned.")
        except:
            bot.send_message(ADMIN_ID, "⚠️ Invalid command. Use: `/unban <user_id>`", parse_mode="Markdown")

@bot.message_handler(commands=['warn'])
def warn_user(message):
    if message.chat.id == ADMIN_ID:
        try:
            user_id = int(message.text.split()[1])
            bot.send_message(user_id, "⚠️ wᴀʀɴιɴԍ! ᴘʟᴇᴀsᴇ ғoʟʟow тнᴇ ʀuʟᴇs.")
            bot.send_message(ADMIN_ID, f"⚠️ User {user_id} has been *warned*.")
        except:
            bot.send_message(ADMIN_ID, "⚠️ Invalid command. Use: `/warn <user_id>`", parse_mode="Markdown")
            
import time

# /restart Command with Animation
@bot.message_handler(commands=['restart'])
def restart_command(message):
    chat_id = message.chat.id

    # Step 1: Sending Initial Restart Animation
    restart_msg = bot.send_message(chat_id, "♻️ **ʀᴇsтᴀʀтιɴԍ...**", parse_mode="Markdown")
    time.sleep(1)

    # Step 2: Animated Restart Process
    animation_steps = [
        "🔄 **ʀᴇʙooтιɴԍ sʏsтᴇм...**",
        "⚙️ **oᴘтιмιzιɴԍ ᴘᴇʀғoʀмᴀɴcᴇ...**",
        "🔋 **cнᴇcκιɴԍ ᴘowᴇʀ ʟᴇvᴇʟs...**",
        "✅ **ᴀʟʟ sʏsтᴇмs oɴʟιɴᴇ!**"
    ]

    for step in animation_steps:
        bot.edit_message_text(step, chat_id, restart_msg.message_id, parse_mode="Markdown")
        time.sleep(1)

    # Step 3: Sending Final Restart Message
    bot.edit_message_text("🚀 **ʀᴇsтᴀʀт succᴇssғuʟ!**\n\n🔹 *ʙoт ιs ɴow oɴʟιɴᴇ ᴀɴᴅ ғuʟʟʏ ғuɴcтιoɴᴀʟ.*", chat_id, restart_msg.message_id, parse_mode="Markdown")

DATA_FILE = "user_messages.txt"  # File to store user messages

# Load stored messages from file
def load_messages():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save messages to file
def save_messages(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Load existing messages
user_messages = load_messages()

@bot.message_handler(commands=['clear', 'delete', 'clean'])
def confirm_delete(message):
    """Asks the user to confirm before deleting all messages."""
    chat_id = str(message.chat.id)

    if chat_id not in user_messages:
        user_messages[chat_id] = []
    user_messages[chat_id].append(message.message_id)
    save_messages(user_messages)

    # Create inline buttons
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("✅ ʏᴇs", callback_data=f"delete_all_{chat_id}"),
        InlineKeyboardButton("❌ ɴo", callback_data=f"delete_current_{message.message_id}")
    )

    # Send confirmation message and track it
    sent_msg = bot.send_message(chat_id, "ᴀʀᴇ ʏou suʀᴇ ʏou wᴀɴт тo ᴅᴇʟᴇтᴇ ᴀʟʟ cнᴀт?", reply_markup=keyboard)
    user_messages[chat_id].append(sent_msg.message_id)
    save_messages(user_messages)

ADMIN_CHAT_ID = '7858368373'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.username
    user_id = message.from_user.id
    
    markup = types.InlineKeyboardMarkup()
    support_button = types.InlineKeyboardButton("suᴘᴘoʀт", url="https://t.me/ARMANTEAMVIP")
    developer_button = types.InlineKeyboardButton("ᴅᴇvᴇʟoᴘᴇʀ", url="https://t.me/MR_INDIAN_OWNER_1")
    markup.add(support_button, developer_button)
    
    welcome_message = "👋 нᴇʟʟo, ι ᴀм ᴀ **тᴇxт-тo-sᴘᴇᴇcн ʙoт**!\n\n🎤 **sᴇɴᴅ мᴇ ᴀɴʏ тᴇxт, ᴀɴᴅ ι'ʟʟ coɴvᴇʀт ιт ιɴтo sᴘᴇᴇcн!**"
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)
    
    admin_message = f"new user joined\nusername: {username}\nuser id: {user_id}"
    bot.send_message(ADMIN_CHAT_ID, admin_message)


@bot.message_handler(commands=['help'])
def help_message(message):
    help_text = (
        "🎤 **Text-to-Speech Bot Guide:**\n\n"
        "🔹 Send me any text, and I'll convert it into a **realistic male voice** audio.\n"
        "🔹 Supports **multiple languages** (default: English)\n"
        "🔹 Processing is **ultra-fast** with a loading animation\n"
        "🔹 Works in **private chat & groups**\n\n"
        "**Commands:**\n"
        "✅ `/start` - Start the bot\n"
        "✅ `/help` - Show this help message\n\n"
        "💡 Try it now! Just send me a text message."
    )

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔹 coɴтᴀcт suᴘᴘoʀт", url="https://t.me/MR_INDIAN_OWNER_1"))

    bot.send_message(message.chat.id, help_text, reply_markup=keyboard, parse_mode="Markdown")

# Process Text and Convert to Speech
@bot.message_handler(func=lambda message: True)
def convert_text_to_speech(message):
    chat_id = message.chat.id
    text = message.text

    # Loading Animation
    loading_msg = bot.send_message(chat_id, "🎙️ **ᴘʀocᴇssιɴԍ... ᴘʟᴇᴀsᴇ wᴀιт**", parse_mode="Markdown")
    time.sleep(1)  # Simulate quick processing time

    # Convert Text to Speech
    try:
        tts = gtts.gTTS(text, lang="en", slow=False)
        audio_file = f"{AUDIO_PATH}/{chat_id}_{int(time.time())}.mp3"
        tts.save(audio_file)

        # Delete Loading Message
        bot.delete_message(chat_id, loading_msg.message_id)

        # Send the Audio File
        with open(audio_file, "rb") as audio:
            bot.send_voice(chat_id, audio, caption="🎧 нᴇʀᴇ ιs ʏouʀ ᴀuᴅιo !")

        # Cleanup
        os.remove(audio_file)
    except Exception as e:
        bot.send_message(chat_id, "⚠️ **Error generating audio!** Please try again.")



@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_all_") or call.data.startswith("delete_current_"))
def handle_callback(call):
    chat_id = str(call.message.chat.id)

    if call.data.startswith("delete_all_"):
        # Delete all stored messages for the user
        if chat_id in user_messages:
            for msg_id in user_messages[chat_id]:  
                try:
                    bot.delete_message(int(chat_id), msg_id)
                except:
                    pass
            user_messages[chat_id] = []  # Clear message history
            save_messages(user_messages)

        bot.send_message(int(chat_id), "✅ ᴀʟʟ cнᴀт мᴇssᴀԍᴇs ᴅᴇʟᴇтᴇᴅ!")

    elif call.data.startswith("delete_current_"):
        # Delete only the confirmation message
        msg_id = int(call.data.split("_")[2])
        try:
            bot.delete_message(int(chat_id), msg_id)
            bot.delete_message(int(chat_id), call.message.message_id)
        except:
            pass

# Track all user & bot messages in private chat
@bot.message_handler(func=lambda message: message.chat.type == "private")
def track_messages(message):
    chat_id = str(message.chat.id)
    
    if chat_id not in user_messages:
        user_messages[chat_id] = []
    user_messages[chat_id].append(message.message_id)
    save_messages(user_messages)
    


# Run the bot
bot.polling()
