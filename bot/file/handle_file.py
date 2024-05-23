import json
import os
import aiohttp
import traceback
from telegram import Update, InputMediaPhoto, error

from ai.normalizers import normalize_gpt_4o_result, normalize_message_result, strip_html_tags
from ai.request import send_to_chatgpt_vision
from ai.messages import GREETING_MESSAGE
from menu import render_main_menu
from file.pdf import pdf_to_images
from logger import logger

FILE_FORMAT_ERROR = "🔴 Загруженный файл не является PDF документом или изображением. Загрузите пожалуйста допустимый файл."
UPLOADED_PDF = "✅ Вы загрузили PDF файл."
UPLOADED_IMAGE = "✅ Вы загрузили изображение."

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

async def download_file(file_url, destination):
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            if response.status == 200:
                with open(destination, 'wb') as f:
                    f.write(await response.read())
            else:
                logger.error(f"Failed to download file from {file_url}")

async def handle_file(update: Update, context):
    if context.user_data.get('expecting_file'):
        file = await update.message.document.get_file() or await update.message.photo[-1].get_file()

        logger.info(f"Received file: {file.file_path}")

        if not update.message.document and not update.message.photo:
            await update.message.reply_text(FILE_FORMAT_ERROR)
            return

        if update.message.document:
            mime_type = update.message.document.mime_type

            if mime_type != 'application/pdf' and not mime_type.startswith('image/'):
                await update.message.reply_text(FILE_FORMAT_ERROR)
                return

            if mime_type == 'application/pdf':
                local_file_path = os.path.join('/tmp', os.path.basename(file.file_path))

                await update.message.reply_text('✅ Вы загрузили PDF файл. Пожалуйста, подождите, идет обработка...')

                try:
                    await download_file(file.file_path, local_file_path)
                    images = pdf_to_images(local_file_path)

                    logger.info(f"PDF file was successfully converted to images: {images}")
                    
                    media = []
                    image_paths = []
                    for image_index, image in enumerate(images):
                        temp_image_path = f"/tmp/temp_image_{image_index}.png"
                        image.save(temp_image_path, format="PNG")
                        image_paths.append(temp_image_path)
                        media.append(InputMediaPhoto(open(temp_image_path, 'rb')))

                    await update.message.reply_media_group(media=media)

                    await update.message.reply_text(GREETING_MESSAGE, parse_mode='HTML', disable_web_page_preview=True)

                    ai_response = await send_to_chatgpt_vision(image_paths)
                    ai_content = json.loads(ai_response['choices'][0]['message']['content'])

                    for idx, result in enumerate(ai_content['results']):
                        normalized_result = normalize_gpt_4o_result(result)
                        message = normalize_message_result(normalized_result)
                        try:
                            await update.message.reply_text(message, parse_mode='HTML', disable_web_page_preview=True)
                        except error.BadRequest:
                            stript_message = strip_html_tags(message)
                            await update.message.reply_text(stript_message, disable_web_page_preview=True)

                    ps_text = f"Необходама консультация врача: <a href='https://lilystarfit.com'>получить консультацию</a>\n"
                    await update.message.reply_text(ps_text, parse_mode='HTML', disable_web_page_preview=True)

                    context.user_data['expecting_file'] = False
                    os.remove(local_file_path)
                    for idx in range(len(images)):
                        os.remove(f"/tmp/temp_image_{idx}.png")
                except Exception as e:
                    logger.error(f"Failed to process PDF file: {e}\n{traceback.format_exc()}")
                    await update.message.reply_text("❌ Произошла ошибка при обработке файла. Попробуйте еще раз.")
                    await render_main_menu(update, context)

            elif mime_type.startswith('image/'):
                await update.message.reply_text(UPLOADED_IMAGE)
                context.user_data['expecting_file'] = False

        elif update.message.photo:
            await update.message.reply_text(UPLOADED_IMAGE)
            context.user_data['expecting_file'] = False

            await render_main_menu(update, context)
