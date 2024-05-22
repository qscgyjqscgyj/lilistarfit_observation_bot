import os

from telegram import Update
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, ApplicationBuilder, filters

from bot.menu import render_main_menu, SEND_OBSERVATION_KEY
from bot.file.handle_file import handle_file

TOKEN = os.getenv('TG_BOT_TOKEN', None)

PLEASE_UPLOAD_FILE = "🟢 Пожалуйста загрузите PDF файл или изображение."

async def start(update: Update, context):
    await render_main_menu(update, context)

async def button(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    if query.data == SEND_OBSERVATION_KEY:
        context.user_data['expecting_file'] = True
        await query.edit_message_text(text=PLEASE_UPLOAD_FILE)

def run():
    app = ApplicationBuilder().token(TOKEN).concurrent_updates(True).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, handle_file))

    app.run_polling()

run()
