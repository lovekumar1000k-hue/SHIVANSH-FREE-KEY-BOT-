import os, json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("8806861845:AAHly2w7sdDvOqY8tDKzZKrb6DAlhKVkdH8")
OWNER_ID = 7513572013

def load():
    try:
        with open("data.json","r") as f: return json.load(f)
    except:
        return {"slots": {str(i): None for i in range(1,8)}, "verify_link": None, "admins": [OWNER_ID]}
def save(d):
    with open("data.json","w") as f: json.dump(f, d)

db = load()
if OWNER_ID not in db["admins"]: db["admins"].append(OWNER_ID)
def is_admin(uid): return uid in db["admins"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Board khud banayega 1 se 7 tak
    btns = []
    row = []
    for i in range(1,8):
        link = db["slots"].get(str(i)) or db["slots"].get("1") or "https://t.me/"
        row.append(InlineKeyboardButton(f"Channel {i}", url=link))
        if len(row)==3:
            btns.append(row); row=[]
    if row: btns.append(row)

    v_link = db["verify_link"] or db["slots"].get("1") or "https://t.me/"
    btns.append([InlineKeyboardButton("✅ Verify / Check Joined", url=v_link)])
    btns.append([InlineKeyboardButton("🔑 Get Key", callback_data="getkey")])

    if is_admin(update.effective_user.id):
        btns.append([InlineKeyboardButton("⚙️ Board Panel", callback_data="admin")])

    await update.message.reply_text(f"MR SANTU OFFICCIAL\n619 monthly users\n1 se 7 tak Auto Board:", reply_markup=InlineKeyboardMarkup(btns))

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text.strip()

    if text.startswith("/addadmin") and uid == OWNER_ID:
        try:
            nid = int(text.split()[1])
            if nid not in db["admins"]:
                db["admins"].append(nid); save(db)
                await update.message.reply_text(f"✅ {nid} Admin ban gaya")
            else: await update.message.reply_text("Pehle se admin hai")
        except: await update.message.reply_text("Use: /addadmin 123456789")
        return

    if not is_admin(uid): return

    # /setall se 1 se 7 tak ek sath lag jayega - BOARD KHUD BANAYEGA
    if text.startswith("/setall") and "t.me/" in text:
        link = text.split()[-1]
        for i in range(1,8): db["slots"][str(i)] = link
        db["verify_link"] = link
        save(db)
        await update.message.reply_text(f"✅ Board ne khud bana diya!\n1 se 7 + Verify sab pe = {link}\n\n/start dabao")
        return

    if text.upper().startswith("SLOT ") and text.upper().split()[-1].isdigit():
        slot = text.upper().split()[-1]
        if 1 <= int(slot) <= 7:
            await update.message.reply_text(f"SLOT {slot} ke liye link bhejo is tarah:\n/setslot {slot} https://t.me/+link")
        return

    if text.startswith("/setslot") and "t.me/" in text:
        try:
            parts = text.split()
            slot = parts[1]
            link = parts[2]
            db["slots"][slot] = link
            save(db)
            await update.message.reply_text(f"✅ SLOT {slot} pe lag gaya: {link}")
        except: await update.message.reply_text("Use: /setslot 1 https://t.me/+link")
        return

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    if q.data == "admin":
        await q.message.reply_text(f"Board Panel\nAdmins: {db['admins']}\n\n1 se 7 tak ek sath lagana:\n/setall https://t.me/+link\n\nAlag alag lagana:\n/setslot 1 link\n/setslot 2 link\n...\n/setslot 7 link\n\nDost ko admin:\n/addadmin ID")
    elif q.data == "getkey":
        await q.message.reply_text(f"✅ Verified\n🔑 Key: DRIP-FREE-KEY-123")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addadmin", text_handler))
app.add_handler(CommandHandler("setall", text_handler))
app.add_handler(CommandHandler("setslot", text_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
app.add_handler(CallbackQueryHandler(callback_handler))
app.run_polling()
