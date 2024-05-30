from telegram import InlineKeyboardButton, InlineKeyboardMarkup


SEND_OBSERVATION_KEY = "send_observation"
ANALYSES_KEY = "analyses"
THEORY_KEY = "theory"


def get_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "Получить расшифровку", callback_data=SEND_OBSERVATION_KEY
            )
        ],
        [InlineKeyboardButton("Сдать анализы", url="https://www.google.com")],
        [InlineKeyboardButton("Теория", url="https://www.google.com")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def render_main_menu(update, context):
    reply_markup = get_menu_keyboard()
    await update.message.reply_text(
        "Выберите один из вариантов: ", reply_markup=reply_markup
    )
