import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "10000"))


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

    def log_message(self, format, *args):
        pass


def run_web_server():
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    server.serve_forever()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📋 Tasks", callback_data="tasks"),
            InlineKeyboardButton("🛍️ Services", callback_data="services"),
        ],
        [
            InlineKeyboardButton("💰 Balance", callback_data="balance"),
            InlineKeyboardButton("👥 Referral", callback_data="referral"),
        ],
        [
            InlineKeyboardButton("💸 Withdraw", callback_data="withdraw"),
            InlineKeyboardButton("📜 History", callback_data="history"),
        ],
        [
            InlineKeyboardButton("📞 Support", callback_data="support")
        ],
    ]

    await update.message.reply_text(
        "স্বাগতম! 👋\n\nBD Digital Service & Task Bot-এ আপনাকে স্বাগতম।",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    messages = {
        "tasks": "📋 Available Tasks\n\nবর্তমানে কোনো Task নেই।",
        "services": "🛍️ Digital Services\n\nবর্তমানে কোনো Service নেই।",
        "balance": "💰 আপনার Balance: 0.00 টাকা",
        "referral": "👥 Referral System শীঘ্রই চালু হবে।",
        "withdraw": "💸 Withdrawal\n\nMinimum withdrawal: 20 টাকা",
        "history": "📜 আপনার কোনো Transaction History নেই।",
        "support": "📞 Support\n\nAdmin-এর সাথে যোগাযোগ করুন।",
    }

    await query.edit_message_text(
        messages.get(query.data, "❌ Unknown option")
    )


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN সেট করা হয়নি")

    threading.Thread(target=run_web_server, daemon=True).start()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()k
