import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 0 # Yaha apni ID daal de @userinfobot se leke

# Channel Links - yahi tu SLOT 1 se set karega
CHANNELS = {
    "Channel 1": None,
    "Channel 2": None,
    "Channel 3": None,
}
user_state = {}

def main_keyboard():
    buttons = []
    # Channel 5,6,7 tere photo jaise
    buttons.append([
        InlineKeyboardButton("Channel 5", url=CHANNELS["Channel 1"] or "https://t.me/"),
        InlineKeyboardButton("Channel 6", url=CHANNELS["Channel 2"] or "https://t.me/")
    ])
    buttons.append([InlineKeyboardButton("Channel 7", url=CHANNELS["Channel 3"] or "https://t.me/")])
    buttons.append([InlineKeyboardButton("Check Joined", callback_data="check")])
    buttons.append([InlineKeyboardButton("🔑 Get Key", callback_data="getkey")])
    return InlineKeyboardMarkup(buttons)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "MR SANTU OFICCIAL\nSabhi Channel Join Karo:",
        reply_markup=main_keyboard()
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text.strip()

    # ADMIN PANEL - SLOT 1
    if text.upper() == "SLOT 1":
        user_state[uid] = "WAIT_CH_1"
        await update.message.reply_text("📌 Send Channel 1 Link Now")
        return

    if uid in user_state:
        state = user_state[uid]
        if text.startswith("https://t.me/"):
            if state == "WAIT_CH_1":
                CHANNELS["Channel 1"] = text
                user_state[uid] = "WAIT_CH_2"
                await update.message.reply_text(f"✅ Channel 1 Set\n\n📌 Send Channel 2 Link Now")
                return
            elif state == "WAIT_CH_2":
                CHANNELS["Channel 2"] = text
                user_state[uid] = "WAIT_CH_3"
                await update.message.reply_text(f"✅ Channel 2 Set\n\n📌 Send Channel 3 Link Now")
                return
            elif state == "WAIT_CH_3":
                CHANNELS["Channel 3"] = text
                user_state.pop(uid)
                await update.message.reply_text(f"✅ Channel 3 Set\n\nAll Done! /start dabao", reply_markup=main_keyboard())
                return

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "check":
        await query.message.reply_text("✅ Checked! Sab channels joined hai.")
    if query.data == "getkey":
        await query.message.reply_text("✅ SLOT 1\n🔑 Your Key: DRIP-CLINE-KEY-1")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
app.add_handler(CallbackQueryHandler(callback_handler))
print("Bot Started @free_key_all_panel_use_bot")
app.run_polling()
