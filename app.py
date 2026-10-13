import os
import asyncio
import logging
import threading

from flask import Flask, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

BOT_TOKEN = "8696872475:AAGICNVhr1hDslMe_PAsvozGOiO0hPG5u3s"
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/hayato_codex").strip()
WELCOME_TEXT = os.getenv(
    "WELCOME_TEXT",
    "⚡ WELCOME TO HAYATO CODEX ⚡\\n\\n"
    "Assalam-o-Alaikum {first_name}! 👋\\n\\n"
    "🤖 Welcome to HAYATO CODEX BOT.\\n"
    "📢 Join our official channel for updates and announcements.\\n\\n"
    "💠 Powered by HAYATO CODEX\\n"
    "🚀 Fast • Smart • Reliable",
)

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN missing. Set it in hosting environment variables.")

web = Flask(__name__)
telegram_app = Application.builder().token(BOT_TOKEN).build()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    first_name = user.first_name if user and user.first_name else "there"
    message = WELCOME_TEXT.replace("{first_name}", first_name)
    keyboard = [[InlineKeyboardButton("📢 Join HAYATO CODEX", url=CHANNEL_URL)]]
    if update.effective_message:
        await update.effective_message.reply_text(
            message, reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message:
        await update.effective_message.reply_text(
            "Available commands:\\n/start — Welcome message\\n/help — Show this help"
        )

telegram_app.add_handler(CommandHandler("start", start_command))
telegram_app.add_handler(CommandHandler("help", help_command))

@web.get("/")
def home():
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        "<title>HAYATO CODEX Bot</title></head>"
        "<body style='font-family:Arial,sans-serif;max-width:720px;margin:60px auto;"
        "padding:0 20px;background:#101018;color:#f5f5ff'>"
        "<h1>⚡ HAYATO CODEX</h1><p>Telegram bot service status page.</p>"
        "<p><a style='color:#8ab4ff' href='/health'>Check health</a></p></body></html>",
        200, {"Content-Type": "text/html; charset=utf-8"}
    )

@web.get("/health")
def health():
    return jsonify(status="ok", service="hayato-codex-telegram-bot"), 200

def run_telegram_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    telegram_app.run_polling(drop_pending_updates=False, close_loop=False)

def start_bot_thread():
    threading.Thread(target=run_telegram_bot, name="telegram-bot", daemon=True).start()

start_bot_thread()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    web.run(host="0.0.0.0", port=port)
