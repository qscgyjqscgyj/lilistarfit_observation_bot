import json
import os
from PIL import Image
import traceback
from telegram import File, InputMediaPhoto, Update, error as tg_error
from ai.messages import GREETING_MESSAGE
from ai.openai import get_observation_results, get_observation_values
from ai.normalizers import (
    normalize_observation_interpretation_result,
    normalize_message_result,
    strip_html_tags,
)
from file.utils import download_file
from logger import logger


async def handle_image_files(update: Update, context, images):
    try:
        media = []
        image_paths = []
        for image in images:
            local_image_path = None

            if type(image) == Image:
                local_image_path = image.file_path

            if type(image) == File:
                local_image_path = os.path.join(
                    "/tmp", os.path.basename(image.file_path)
                )
                await download_file(image.file_path, local_image_path)

            if local_image_path:
                image_paths.append(local_image_path)
                media.append(InputMediaPhoto(open(local_image_path, "rb")))

        await update.message.reply_text(
            GREETING_MESSAGE, parse_mode="HTML", disable_web_page_preview=True
        )

        ai_response_data = get_observation_values(image_paths)

        for result in ai_response_data["results"]:
            normalized_result = normalize_observation_interpretation_result(result)
            message = normalize_message_result(normalized_result)
            try:
                await update.message.reply_text(
                    message, parse_mode="HTML", disable_web_page_preview=True
                )
            except tg_error.BadRequest:
                stript_message = strip_html_tags(message)
                await update.message.reply_text(
                    stript_message, disable_web_page_preview=True
                )

        ps_text = f"Необходама консультация врача: <a href='https://lilystarfit.com'>получить консультацию</a>\n"
        await update.message.reply_text(
            ps_text, parse_mode="HTML", disable_web_page_preview=True
        )

        context.user_data["expecting_file"] = False

        for image_path in image_paths:
            os.remove(image_path)
    except Exception as e:
        logger.error(f"Failed to process Image file: {e}\n{traceback.format_exc()}")
        await update.message.reply_text(
            "❌ Произошла ошибка при обработке изображения. Попробуйте еще раз."
        )
