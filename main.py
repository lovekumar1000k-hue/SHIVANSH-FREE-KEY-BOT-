import os, threading
from flask import Flask
from telegram import Update, ChatMemberAdministrator
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ChatMemberStatus

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Render me ye token dalna: 8871444371:AAFAUpLj597wDomf-RKLmkWJ35C7qDKbjbg
# NOTE: Baad me token revoke karke naya dal dena

app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "Fake Owner Bot is Live"
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

async def setowner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message and len(context.args) == 0:
        await update.message.reply_text("Use: /setowner @username ya kisi ke message pe reply karke /setowner likho")
        return
    
    try:
        if update.message.reply_to_message:
            user_id = update.message.reply_to_message.from_user.id
        else:
            username = context.args[0].replace("@","")
            user = await context.bot.get_chat(username)
            user_id = user.id

        # Admin banao + Owner title do
        await context.bot.promote_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_promote_members=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True
        )
        await context.bot.set_chat_administrator_custom_title(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            custom_title="Owner ❤️"
        )
        await update.message.reply_text(f"✅ Done! Ab ye banda Owner dikhega! 👑")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}\n\nBot ko Admin banao aur 'Add new admins' ka permission do.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👑 Fake Owner Bot Ready!\n\nKisi ko Owner dikhana hai to:\n/setowner @username\n\nYa uske message pe reply karke /setowner likho")

def main():
    threading.Thread(target=run_flask).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setowner", setowner))
    app.add_handler(CommandHandler("owner", setowner))
    print("Bot Started...")
    app.run_polling()

if __name__ == "__main__":
    main()
