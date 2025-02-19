import telebot
import time
import threading
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "7686091578:AAEr8ZECqpAo1bqxaj6fP91Ka0zRS9yU3BU"
ADMIN_ID = 7858368373

bot = telebot.TeleBot(BOT_TOKEN)

repeat_cache = {}
processing_messages = {}
banned_users = set()
user_data = {}
DATA_FILE = "user_messages.txt"

def load_messages():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_messages(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


user_messages = load_messages()


def notify_admin(text):
    """Send a notification to the admin"""
    bot.send_message(ADMIN_ID, f"⚠️ {text}")

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    username = message.from_user.username or "Unknown"
    
    if user_id not in user_data:
        user_data[user_id] = username
        notify_admin(f"🆕 New user joined!\n👤 Username: @{username}\n🆔 User ID: {user_id}")

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton("➕ Support Group", url="https://t.me/ARMANTEAMVIP"),
        telebot.types.InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/MR_INDIAN_OWNER_1")
    )
    bot.send_message(user_id, "👋 нι! wᴇʟcoмᴇ тo тнᴇ ʙoт.\nι cᴀɴ ʀᴇᴘᴇᴀт ʏouʀ мᴇssᴀԍᴇs ᴀs мᴀɴʏ тιмᴇs ᴀs ʏou wᴀɴт!", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_command(message):
    user_id = message.chat.id
    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("📩 Contact Support", url="https://t.me/MR_INDIAN_OWNER_1"))
    
    help_text = """
🤖 **ʙoт ғᴇᴀтuʀᴇs**

- ʀᴇᴘᴇᴀт ᴀɴʏ тᴇxт uᴘ тo 1000 тιмᴇs
- ғᴀsт ᴘʀocᴇssιɴԍ wιтн ᴀɴιмᴀтιoɴ
- ᴀᴅмιɴ coммᴀɴᴅs ғoʀ мᴀɴᴀԍιɴԍ usᴇʀs

🔹 **usᴀԍᴇ**

1️⃣ sᴇɴᴅ ᴀɴʏ тᴇxт
2️⃣ ʙoт ᴀsκs нow мᴀɴʏ тιмᴇs тo ʀᴇᴘᴇᴀт
3️⃣ ᴇɴтᴇʀ ᴀ ɴuмʙᴇʀ (1-1000)
4️⃣ ԍᴇт ʏouʀ ʀᴇᴘᴇᴀтᴇᴅ тᴇxт ιɴsтᴀɴтʟʏ! 

🔸 *Admin Commands:*
- `/ban <user_id>` 🚫 Ban user.
- `/unban <user_id>` ✅ Unban user.
- `/warn <user_id>` ⚠️ Warn user.
- `/users` 📜 View all users.
- `/broadcast <text>` 📢 Send message to all users.
"""
    bot.send_message(user_id, help_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.chat.id == ADMIN_ID:
        try:
            user_id = int(message.text.split()[1])
            banned_users.add(user_id)
            bot.send_message(user_id, "🚫 ʏou нᴀvᴇ ʙᴇᴇɴ **ʙᴀɴɴᴇᴅ** ғʀoм usιɴԍ тнιs ʙoт.", parse_mode="Markdown")
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
            bot.send_message(user_id, "⚠️ Warning! Please follow the rules.")
            bot.send_message(ADMIN_ID, f"⚠️ User {user_id} has been *warned*.")
        except:
            bot.send_message(ADMIN_ID, "⚠️ Invalid command. Use: `/warn <user_id>`", parse_mode="Markdown")

import time

# /restart Command with Animation
@bot.message_handler(commands=['restart'])
def restart_command(message):
    chat_id = message.chat.id

    # Step 1: Sending Initial Restart Animation
    restart_msg = bot.send_message(chat_id, "♻️ **Restarting...**", parse_mode="Markdown")
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
    bot.edit_message_text("🚀 **ʀᴇsтᴀʀт succᴇssғuʟ!**\n\n🔹 **ʙoт ιs ɴow oɴʟιɴᴇ ᴀɴᴅ ғuʟʟʏ ғuɴcтιoɴᴀʟ**", chat_id, restart_msg.message_id, parse_mode="Markdown")
    
    
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


@bot.message_handler(commands=['users'])
def list_users(message):
    if message.chat.id == ADMIN_ID:
        if user_data:
            user_list = "\n".join([f"👤 @{username} | 🆔 {uid}" for uid, username in user_data.items()])
            bot.send_message(ADMIN_ID, f"📜 *All Users:*\n\n{user_list}", parse_mode="Markdown")
        else:
            bot.send_message(ADMIN_ID, "⚠️ No users found.")

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.chat.id == ADMIN_ID:
        text = message.text.replace("/broadcast ", "")
        if text.strip():
            for user_id in user_data.keys():
                try:
                    bot.send_message(user_id, f"📢 *Broadcast Message:*\n{text}", parse_mode="Markdown")
                except:
                    pass
            bot.send_message(ADMIN_ID, "✅ Broadcast sent successfully!")
        else:
            bot.send_message(ADMIN_ID, "⚠️ Use: `/broadcast <message>`")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id

    if user_id in banned_users:
        bot.send_message(user_id, "🚫 You are banned from using this bot.")
        return

    username = message.from_user.username or "Unknown"

    if user_id in repeat_cache:
        try:
            count = int(message.text)

            if 1 <= count <= 2000:
                text = repeat_cache[user_id]
                del repeat_cache[user_id]

                processing_msg = bot.send_message(user_id, "🔄 Processing...")
                processing_messages[user_id] = [processing_msg.message_id]

                progress = bot.send_message(user_id, "⏳ Progress: [░░░░░░░░░░] 0%")
                processing_messages[user_id].append(progress.message_id)

                for i in range(1, 11):
                    time.sleep(0.2)
                    bar = "█" * i + "░" * (10 - i)
                    bot.edit_message_text(f"⏳ Progress: [{bar}] {i*10}%", user_id, progress.message_id)

                repeated_text = "\n".join([text] * count)
                bot.send_message(user_id, f"```python\n{repeated_text}\n```", parse_mode="Markdown")

                for msg_id in processing_messages.get(user_id, []):
                    bot.delete_message(user_id, msg_id)

                notify_admin(f"🔁 *New Text Repeated*\n👤 @{username}\n📄 Text: `{text}`\n🔢 Times: {count}")

            else:
                bot.send_message(user_id, "⚠️ Enter a number between 1 and 1,000.")
        except ValueError:
            bot.send_message(user_id, "⚠️ Invalid input! Please enter a number.")
    else:
        repeat_cache[user_id] = message.text
        msg = bot.send_message(user_id, "💬 How many times to repeat? (1 - 1000)")
        processing_messages[user_id] = [msg.message_id]
        
        
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

        bot.send_message(int(chat_id), "✅ All chat messages deleted!")

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

print("🚀 Bot is running...")


print("🚀 Bot is running...")
bot.infinity_polling()
