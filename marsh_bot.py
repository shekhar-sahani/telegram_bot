from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_TOKEN

# Replace 'YOUR_BOT_TOKEN' with the token you received from BotFather
BOT_TOKEN = TELEGRAM_TOKEN

print('telegramToken---> ', BOT_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Hello! I'm your bot. How can I help you?")

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()
    
    if "hello" in user_message:
        await update.message.reply_text("Hi there! How can I help you is there something I can assist you with?")
    else:
        await update.message.reply_text(f"You said: {user_message}")

def main():
    # Create the Application instance
    application = Application.builder().token(BOT_TOKEN).build()

    # Define command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
