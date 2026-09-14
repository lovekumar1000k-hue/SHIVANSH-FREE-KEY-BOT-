import os, json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("8806861845:AAHly2w7sdDvOqY8tDKzZKrb6DAlhKVkdH8")

def load():
    try:
        with open("data.json","r") as f: return json.load(f)
    except:
        return {
            "slots": {str(i): [] for i in range(1,8)}, # 1 to 7
            "check_channels": [],
            "key_channel": None,
            "state": {}
        }

def save(d):
    with open("data.json","w") as f: json.dump(f, d)

db = load()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # SLOT 1 to 7 ke buttons
    btns = []
    row = []
    for i in range(1,8):
        row.append(InlineKeyboardButton(f"SLOT {i}", callback_data=f"slot_{i}"))
        if len(row)==3:
            btns.append(row); row=[]
    if row: btns.append(row)
    btns.append([InlineKeyboardButton("⚙️ Admin: SET CHECK & KEY", callback_data="admin_help")])
    await update.message.reply_text("MR SANTU OFFICCIAL\nSlot select karo:", reply_markup=InlineKeyboardMarkup(btns))

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global db
    uid = str(update.effective_user.id)
    text = update.message.text.strip()

    # ADMIN COMMANDS
    # SLOT 1, SLOT 2... SLOT 7
    if text.upper().startswith("SLOT ") and text.upper().split()[-1].isdigit():
        slot = text.upper().split()[-1]
        if 1 <= int(slot) <= 7:
            db["state"][uid] = f"WAIT_SLOT_{slot}"
            db["slots"][slot] = [] # purana clear
            save(db)
            await update.message.reply_text(f"📌 SLOT {slot} ke liye Channel Link bhejo\nEk ek karke bhejo. Ho jaye to DONE likho.\n\nAbhi: Send Channel Link for SLOT {slot}")
            return

    if text.upper() == "SET CHECK":
        db["state"][uid] = "WAIT_CHECK"
        db["check_channels"] = []
        save(db)
        await update.message.reply_text("📌 Check Joined ke liye Channel Link bhejo (DONE likho jab ho jaye)")
        return

    if text.upper() == "SET KEY":
        db["state"][uid] = "WAIT_KEY"
        save(db)
        await update.message.reply_text("📌 Get Key wala Channel Link bhejo")
        return

    if text.upper() == "DONE" and uid in db["state"]:
        del db["state"][uid]
        save(db)
        await update.message.reply_text("✅ Saved Permanent! /start dabao")
        return

    # Link save karna
    if uid in db["state"] and "t.me/" in text:
        st = db["state"][uid]
        if st.startswith("WAIT_SLOT_"):
            slot = st.split("_")[-1]
            db["slots"][slot].append(text)
            save(db)
            await update.message.reply_text(f"✅ SLOT {slot} me add: {text}\nAgla bhejo ya DONE likho")
        elif st == "WAIT_CHECK":
            db["check_channels"].append(text)
            save(db)
            await update.message.reply_text(f"✅ Check me add: {text}\nAgla bhejo ya DONE likho")
        elif st == "WAIT_KEY":
            db["key_channel"] = text
            del db["state"][uid]
            save(db)
            await update.message.reply_text(f"✅ Get Key Channel Set: {text}")
        return

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global db
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("slot_"):
        slot = data.split("_")[1]
        ch_links = db["slots"].get(slot, [])
        if not ch_links:
            await query.message.reply_text(f"❌ SLOT {slot} khali hai. Admin se SLOT {slot} set karwao")
            return
        # Is slot ke channels dikhao
        btns = []
        for idx, link in enumerate(ch_links, 1):
            btns.append([InlineKeyboardButton(f"Channel {idx}", url=link)])
        # Check Joined ke channels
        for link in db["check_channels"]:
            btns.append([InlineKeyboardButton(f"Join Channel", url=link)])
        if db["key_channel"]:
            btns.append([InlineKeyboardButton("🔑 Get Key Channel", url=db["key_channel"])])
        btns.append([InlineKeyboardButton("Check Joined", callback_data=f"check_{slot}")])
        btns.append([InlineKeyboardButton("🔑 Get Key", callback_data=f"getkey_{slot}")])
        await query.message.reply_text(f"👋 SLOT {slot} - 619 users\nSab join karo:", reply_markup=InlineKeyboardMarkup(btns))

    elif data.startswith("getkey_"):
        slot = data.split("_")[1]
        await query.message.reply_text(f"✅ SLOT {slot}\n🔑 Your Key: DRIP-SLOT{slot}-KEY-{len(db['slots'][slot])}\n\nPermanent Bot by MR SANTU")

    elif data == "admin_help":
        await query.message.reply_text("Admin Commands:\nSLOT 1 / SLOT 2... SLOT 7\nSET CHECK\nSET KEY\nDONE")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
app.add_handler(CallbackQueryHandler(callback_handler))
app.run_polling()
