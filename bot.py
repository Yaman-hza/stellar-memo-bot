
import json
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

import os

TOKEN = os.getenv("TOKEN")
STELLAR_ADDRESS = "GBWQQ6BH345ER3B5GXD4I2LDUDNE7YIITQ34FIY7JH2HLFCG27Q6L54Q"
DATA_FILE = "users.json"

def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

def get_menu():
    return ReplyKeyboardMarkup(
        [["Stellar Address", "Memo Code"]],
        resize_keyboard=True
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبًا! اختر من القوائم أدناه:",
        reply_markup=get_menu()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = str(update.message.from_user.id)
    users = load_users()

    if text == "Stellar Address":
        await update.message.reply_text(f"العنوان:
`{STELLAR_ADDRESS}`", parse_mode="Markdown")

    elif text == "Memo Code":
        if user_id in users:
            memo = users[user_id]
        else:
            memo = f"{len(users)+1:05d}"
            users[user_id] = memo
            save_users(users)
        await update.message.reply_text(f"رمز الميمو الخاص بك: `{memo}`", parse_mode="Markdown")

    else:
        await update.message.reply_text("يرجى اختيار خيار من القوائم.", reply_markup=get_menu())

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
