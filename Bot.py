import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📋 Tasks", callback_data="tasks"),
         InlineKeyboardButton("🛍️ Services", callback_data="services")],
        [InlineKeyboardButton("💰 Balance", callback_data="balance"),
         InlineKeyboardButton("👥 Referral", callback_data="referral")],
        [InlineKeyboardButton("💸 Withdraw", callback_data="withdraw"),
         InlineKeyboardButton("📜 History", callback_data="history")],
        [InlineKeyboardButton("📞 Support", callback_data="support")]
    ]

    await update.message.reply_text(
        "স্বাগতম! 👋\n\nBD Digital Service & Task Bot-এ আপনাকে স্বাগতম।",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    messages = {
        "tasks": "📋 Available Tasks\n\nবর্তমানে কোনো Task নেই।",
        "services": "🛍️ Digital Services\n\nবর্তমানে কোনো Service নেই।",
        "balance": "💰 আপনার Balance: 0.00 টাকা",
        "referral": "👥 আপনার Referral Link শীঘ্রই এখানে আসবে।",
        "withdraw": "💸 Withdrawal\n\nMinimum withdrawal: 100 টাকা",
        "history": "📜 আপনার কোনো Transaction History নেই।",
        "support": "📞 Support\n\nসাহায্যের জন্য Admin-এর সাথে যোগাযোগ করুন।"
    }

    await query.edit_message_text(messages.get(query.data, "❌ Unknown option"))

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN সেট করা হয়নি")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
