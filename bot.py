from telebot import TeleBot
from telebot.apihelper import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")

admin_id = int(os.getenv("ADMIN_ID"))

bot = TeleBot(BOT_TOKEN)
user_states = {}


def is_admin(message):
    return message.from_user.id == admin_id


@bot.message_handler(commands=["start"])
def start(message):
    if is_admin(message):
        bot.send_message(
            message.chat.id,
            "👋 Welcome Admin!\n\nUse /create to generate new users."
        )


@bot.message_handler(commands=["create"])
def create(message):
    if is_admin(message):
        chat_id = message.chat.id
        user_states[chat_id] = {}

        bot.send_message(chat_id, "🔢 How many users do you want to create?")
        bot.register_next_step_handler(message, get_user_count)


def get_user_count(message):
    chat_id = message.chat.id
    try:
        user_count = int(message.text)
        if user_count <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(chat_id, "❌ Please enter a valid positive number.")
        return bot.register_next_step_handler(message, get_user_count)

    user_states[chat_id]["user_count"] = user_count
    bot.send_message(chat_id, "🔗 Enter the panel address:")
    bot.register_next_step_handler(message, get_address_panel)


def get_address_panel(message):
    chat_id = message.chat.id
    address_panel = message.text.strip()
    user_states[chat_id]["address"] = address_panel

    bot.send_message(chat_id, "👤 Enter the panel username:")
    bot.register_next_step_handler(message, get_username_panel)


def get_username_panel(message):
    chat_id = message.chat.id
    username_panel = message.text.strip()
    user_states[chat_id]["panel_username"] = username_panel

    bot.send_message(chat_id, "🔑 Enter the panel password:")
    bot.register_next_step_handler(message, get_password_panel)


def get_password_panel(message):
    chat_id = message.chat.id
    password_panel = message.text.strip()
    user_states[chat_id]["panel_password"] = password_panel

    bot.send_message(chat_id, "👤 Enter new users base username:")
    bot.register_next_step_handler(message, get_base_username)


def get_base_username(message):
    chat_id = message.chat.id
    base_username = message.text.strip()
    user_states[chat_id]["base_username"] = base_username

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(KeyboardButton("active"), KeyboardButton("on_hold"))

    bot.send_message(
        chat_id,
        "⚙️ Select user status:",
        reply_markup=markup
    )
    bot.register_next_step_handler(message, get_status_new_user)


def get_status_new_user(message):
    chat_id = message.chat.id
    status = message.text.strip()

    if status not in ["active", "on_hold"]:
        bot.send_message(chat_id, "❌ Please choose one of: active / on_hold")
        return bot.register_next_step_handler(message, get_status_new_user)

    user_states[chat_id]["status"] = status

    if status == "active":
        bot.send_message(chat_id, "⏳ Enter expiration (days, 0 for unlimited):")
        bot.register_next_step_handler(message, get_expire_days)
    else:
        user_states[chat_id]["expire_days"] = 0
        bot.send_message(chat_id, "📦 Enter data limit (GB):")
        bot.register_next_step_handler(message, get_data_limit)


def get_expire_days(message):
    chat_id = message.chat.id
    try:
        expire_days = int(message.text)
        if expire_days < 0:
            raise ValueError
    except ValueError:
        bot.send_message(chat_id, "❌ Please enter a valid number (0 or more).")
        return bot.register_next_step_handler(message, get_expire_days)

    user_states[chat_id]["expire_days"] = expire_days

    bot.send_message(chat_id, "📦 Enter data limit (GB):")
    bot.register_next_step_handler(message, get_data_limit)


def get_data_limit(message):
    chat_id = message.chat.id
    try:
        data_limit_gb = int(message.text)
        if data_limit_gb <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(chat_id, "❌ Please enter a positive number for data limit (GB).")
        return bot.register_next_step_handler(message, get_data_limit)

    user_states[chat_id]["data_limit_gb"] = data_limit_gb

    bot.send_message(chat_id, "📚 Enter group IDs (comma separated, e.g. 1,2,3):")
    bot.register_next_step_handler(message, get_group_ids)


def get_group_ids(message):
    chat_id = message.chat.id
    text = message.text.strip()

    try:
        group_ids = [int(x.strip()) for x in text.split(",") if x.strip()]
        if not group_ids:
            raise ValueError
    except ValueError:
        bot.send_message(chat_id, "❌ Please enter valid group IDs (comma separated numbers).")
        return bot.register_next_step_handler(message, get_group_ids)

    user_states[chat_id]["group_ids"] = group_ids

    status = user_states[chat_id]["status"]

    if status == "on_hold":
        bot.send_message(chat_id, "⏱ Enter on-hold timeout (days):")
        bot.register_next_step_handler(message, get_on_hold_timeout)
    else:
        user_states[chat_id]["on_hold_timeout_days"] = 0
        user_states[chat_id]["on_hold_expire_days"] = 0
        bot.send_message(chat_id, "⏳ Creating users, please wait…")
        create_users_for_chat(chat_id)


def get_on_hold_timeout(message):
    chat_id = message.chat.id
    try:
        days = int(message.text)
        if days <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(chat_id, "❌ Please enter a positive number for on-hold timeout (days).")
        return bot.register_next_step_handler(message, get_on_hold_timeout)

    user_states[chat_id]["on_hold_timeout_days"] = days

    bot.send_message(chat_id, "⌛ Enter on-hold expire duration (days):")
    bot.register_next_step_handler(message, get_on_hold_expire_duration)


def get_on_hold_expire_duration(message):
    chat_id = message.chat.id
    try:
        days = int(message.text)
        if days <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(chat_id, "❌ Please enter a positive number for expire duration (days).")
        return bot.register_next_step_handler(message, get_on_hold_expire_duration)

    user_states[chat_id]["on_hold_expire_days"] = days

    bot.send_message(chat_id, "⏳ Creating users, please wait…")
    create_users_for_chat(chat_id)


def create_users_for_chat(chat_id):
    state = user_states.get(chat_id)
    if not state:
        bot.send_message(chat_id, "⚠️ Session expired. Please start again with /create.")
        return

    user_count = state["user_count"]
    address = state["address"]
    panel_username = state["panel_username"]
    panel_password = state["panel_password"]
    base_username = state["base_username"]
    status = state["status"]
    expire_days = state["expire_days"]
    data_limit_gb = state["data_limit_gb"]
    group_ids = state["group_ids"]
    on_hold_timeout_days = state.get("on_hold_timeout_days", 0)
    on_hold_expire_days = state.get("on_hold_expire_days", 0)

    expire = expire_days
    data_limit = data_limit_gb
    on_hold_timeout = on_hold_timeout_days if on_hold_timeout_days > 0 else None
    on_hold_expire_duration = on_hold_expire_days if on_hold_expire_days > 0 else None

    success_count = 0
    fail_count = 0

    for i in range(user_count):
        username = f"{base_username}-{i+1}"

        payload = {
            "address": address,
            "panel_username": panel_username,
            "panel_password": panel_password,
            "username": username,
            "status": status,
            "expire": expire,
            "data_limit": data_limit,
            "group_ids": group_ids,
            "on_hold_timeout": on_hold_timeout,
            "on_hold_expire_duration": on_hold_expire_duration,
        }

        try:
            resp = requests.post(API_URL, json=payload)
            try:
                data = resp.json()
            except Exception:
                data = {"raw": resp.text}

            if resp.status_code == 200 and data.get("success", True):
                success_count += 1
                bot.send_message(chat_id, f"✅ User {username} created successfully.")
            else:
                fail_count += 1
                bot.send_message(
                    chat_id,
                    f"❌ Failed to create user {username}.\n"
                    f"Status: {resp.status_code}\nResponse: {data}"
                )
        except Exception as e:
            fail_count += 1
            bot.send_message(chat_id, f"❌ Error while creating user {username}:\n{e}")

    bot.send_message(
        chat_id,
        f"📊 Done.\n"
        f"✅ Success: {success_count}\n"
        f"❌ Failed: {fail_count}"
    )
    user_states.pop(chat_id, None)

def start_bot():
    print("🤖 Bot is now running...")
    bot.polling()