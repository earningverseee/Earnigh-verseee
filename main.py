import asyncio
import random
import string
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = 8212417273:AAF56aqx9IkUEoRV0dzwRhIfsLfPaBWy9GU
CHANNELS = ["@+gVZ2fZMJG8VmMDJl", "@+MuDPbnS4NtpiYjdl"]

FILES = {}

def generate_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not context.args:
        await update.message.reply_text("Invalid link!")
        return

    key = context.args[0]

    if key not in FILES:
        await update.message.reply_text("File not found.")
        return

    not_joined = []
    for ch in CHANNELS:
        member = await context.bot.get_chat_member(ch, user.id)
        if member.status in ["left", "kicked"]:
            not_joined.append(ch)

    if not_joined:
        await update.message.reply_text("Join channels first!")
        return

    msg = await update.message.reply_document(FILES[key])

    await asyncio.sleep(1200)

    await context.bot.delete_message(
        chat_id=update.effective_chat.id,
        message_id=msg.message_id
    )

async def save_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document.file_id
    key = generate_key()
    FILES[key] = file

    bot_username = (await context.bot.get_me()).username
    link = f"https://t.me/{bot_username}?start={key}"

    await update.message.reply_text(f"Link:\n{link}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Document.ALL, save_file))

app.run_polling()
