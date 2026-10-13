import os
import threading
import logging
from flask import Flask, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

BOT_TOKEN = os.getenv("8696872475:AAGICNVhr1hDslMe_PAsvozGOiO0hPG5u3s", "").strip()
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/hayato_codex").strip()
WELCOME_TEXT = os.getenv(
    "WELCOME_TEXT",
    "Assalam-o-Alaikum! Bot mein khush aamdeed."
)

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable set nahi hai.")

web = Flask(__name__)
telegram_app = Application.builder().token(BOT_TOKEN).build()
_bot_thread_started = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📢 Hamara Channel", url=https://t.me/hayato_codex)]]
    await update.effective_message.reply_text(
        WELCOME_TEXT,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "Commands:\n/start — Welcome message\n/help — Help"
    )

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("help", help_command))

@web.get("/")
def home():
    return (
        "<h1>Telegram Bot is running</h1>"
        "<p>Health endpoint: <a href='/health'>/health</a></p>",
        200,
        {"Content-Type": "text/html; charset=utf-8"}
    )

@web.get("/health")
def health():
    return jsonify(status="ok", service="telegram-bot"), 200

def run_telegram():
    # Start Telegram polling in a background thread.
    telegram_app.run_polling(
        drop_pending_updates=False,
        close_loop=False
    )

def start_bot_once():
    global _bot_thread_started
    if not _bot_thread_started:
        _bot_thread_started = True
        thread = threading.Thread(target=run_telegram, daemon=True)
        thread.start()

# Start the bot when the web service process starts.
start_bot_once()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    web.run(host="0.0.0.0", port=port)
