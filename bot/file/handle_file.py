import os
from telegram import Update

from file.pdf import handle_pdf_file
from file.image import handle_image_files
from logger import logger

FILE_FORMAT_ERROR = "🔴 Загруженный файл не является PDF документом или изображением. Загрузите пожалуйста допустимый файл."
UPLOADED_PDF = "✅ Вы загрузили PDF файл."
UPLOADED_IMAGE = "✅ Вы загрузили изображение."

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


async def handle_file(update: Update, context):
    if context.user_data.get("expecting_file"):
        file = None

        if update.message.document:
            file = await update.message.document.get_file()
            logger.info(f"Received file: {file.file_path}")

        images = []
        if update.message.photo:
            images = [await photo.get_file() for photo in update.message.photo]
            logger.info(f"Received images: {images}")

        if not update.message.document and not update.message.photo:
            await update.message.reply_text(FILE_FORMAT_ERROR)
            return

        if update.message.document:
            mime_type = update.message.document.mime_type

            if mime_type != "application/pdf" and not mime_type.startswith("image/"):
                await update.message.reply_text(FILE_FORMAT_ERROR)
                return

            if mime_type == "application/pdf":
                await handle_pdf_file(update, context, file)

            elif mime_type.startswith("image/"):
                await handle_image_files(update, context, [file])

        elif update.message.photo:
            await handle_image_files(update, context, images)
