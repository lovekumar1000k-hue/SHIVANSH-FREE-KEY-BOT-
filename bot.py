import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("8806861845:AAGPeXO2hP1Ax3JF55ch4mzt_zX35wENIFQ")
OWNER_ID = int(os.getenv(''8695322804", "0"))

# Sirf owner hi use kar paye
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Ye bot sirf owner ke liye hai.")
        return
    await update.message.reply_text("Bot Live hai Shivansh bhai! ✅")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
