import os
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, ApplicationBuilder, filters

TOKEN = os.getenv('TG_BOT_TOKEN', None)

SEND_OBSERVATION_KEY = 'send_observation'
ANALYSES_KEY = 'analyses'
THEORY_KEY = 'theory'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Получить расшифровку", callback_data=SEND_OBSERVATION_KEY)],
        [InlineKeyboardButton("Сдать анализы", callback_data=ANALYSES_KEY)],
        [InlineKeyboardButton("Теория", callback_data=THEORY_KEY)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(update: Update, context):
    logger.info(f"Button pressed: {update.callback_query.data}")

    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Selected option: {query.data}")

async def handle_file(update: Update, context):
    if context.user_data.get('expecting_file'):
        file = update.message.document or update.message.photo[-1].get_file()

        # Check if the file is a PDF or an image
        if update.message.document:
            mime_type = update.message.document.mime_type
            if mime_type == 'application/pdf':
                await update.message.reply_text("You uploaded a PDF file.")
                context.user_data['expecting_file'] = False
            elif mime_type.startswith('image/'):
                await update.message.reply_text("You uploaded an image file.")
                context.user_data['expecting_file'] = False
            else:
                await update.message.reply_text("The file is neither a PDF nor an image. Please upload a valid file.")
        elif update.message.photo:
            await update.message.reply_text("You uploaded an image file.")
            context.user_data['expecting_file'] = False
        else:
            await update.message.reply_text("The file is neither a PDF nor an image. Please upload a valid file.")

def main():
    app = ApplicationBuilder().token(TOKEN).concurrent_updates(True).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))
    # app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, handle_file))


    app.run_polling()

if __name__ == '__main__':
    main()
