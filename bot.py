import os, json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN") or "8806861845:AAHly2w7sdDvOqY8tDKzZKrb6DAlhKVkdH8"
ADMIN_ID = 5965677114

if os.path.exists("slots.json"):
    with open("slots.json", 'r') as f:
        slots = json.load(f)
else:
    slots = {str(i): "" for i in range(1, 8)}

def save():
    with open("slots.json", 'w') as f:
        json.dump(slots, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    btns = []
    for i in range(1, 8):
        link = slots[str(i)]
        if link:
            btns.append([InlineKeyboardButton(f"Channel {i}", url=link)])
    btns.append([InlineKeyboardButton("Check Joined", callback_data="check")])
    btns.append([InlineKeyboardButton("🔑 Get Key", callback_data="getkey")])
    await update.message.reply_text("👋 MR SANTU OFFICIAL\n\nSabhi Channel Join Karo fir Get Key dabao:", reply_markup=InlineKeyboardMarkup(btns))

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id!= ADMIN_ID: return
    btns = [[InlineKeyboardButton(f"SLOT {i} - {slots[str(i)][:15] if slots[str(i)] else 'Empty'}", callback_data=f"set_{i}")] for i in range(1,8)]
    await update.message.reply_text("Kis Slot me Link Lagana Hai? 👇", reply_markup=InlineKeyboardMarkup(btns))

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data.startswith("set_"):
        no = q.data.split("_")[1]
        context.user_data["wait_for"] = no
        await q.message.reply_text(f"📌 Send Channel {no} Link Now")
    elif q.data == "getkey":
        await q.message.reply_text("🔑 Your Key: `DRIP-CLINE-KEY-1`")

async def save_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "wait_for" in context.user_data:
        no = context.user_data["wait_for"]
        slots[no] = update.message.text.strip()
        save()
        await update.message.reply_text(f"✅ SLOT {no} me save ho gaya")
        del context.user_data["wait_for"]

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CallbackQueryHandler(callback))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_link))
app.run_polling()
