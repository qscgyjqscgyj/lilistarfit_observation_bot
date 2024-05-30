import os
import traceback
from telegram import Update

from file.image import handle_image_files
from file.utils import download_file, pdf_to_images
from logger import logger


async def handle_pdf_file(update: Update, context, file):
    local_file_path = os.path.join("/tmp", os.path.basename(file.file_path))

    await update.message.reply_text(
        "✅ Вы загрузили PDF файл. Пожалуйста, подождите, идет обработка..."
    )

    try:
        await download_file(file.file_path, local_file_path)
        images = pdf_to_images(local_file_path)

        logger.info(f"PDF file was successfully converted to images: {images}")
    except Exception as e:
        logger.error(f"Failed to process PDF file: {e}\n{traceback.format_exc()}")
        await update.message.reply_text(
            "❌ Произошла ошибка при обработке файла. Попробуйте еще раз."
        )

    await handle_image_files(update, context, images)
