import re


def noralize_observation_image_result(result):
    return {
        "name": result.get("name", "Нет данных"),
        "value": result.get("value", "Нет данных"),
    }


def normalize_observation_interpretation_result(result):
    return {
        "name": result.get("name", "Нет данных"),
        "value": result.get("value", "Нет данных"),
        "normsMan": result.get("normsMan", "Нет данных"),
        "normsWoman": result.get("normsWoman", "Нет данных"),
        "description": result.get("description", "Нет данных"),
        "reasons": result.get("reasons", "Нет данных"),
        "conclusion": result.get("conclusion", "Нет данных"),
        "conclusion_code": result.get("conclusion_code", "Нет данных"),
    }


def normalize_message_result(normalized_result):
    result_is_normal = normalized_result["conclusion_code"] == "+"
    result_color = "🟢" if result_is_normal else "🔴"

    reasons_text = (
        ("\n" f"<b>Возможные причиные отклонения</b>: {normalized_result['reasons']}\n")
        if not result_is_normal
        else ""
    )
    conclusion_text = (
        "\n"
        f"<b>{'Рекомендации' if not result_is_normal else 'Заключение' }</b>: {normalized_result['conclusion']}\n"
    )
    consult_advice = (
        ("\n" f"<b>Необходима консультация специалиста!</b>")
        if not result_is_normal
        else ""
    )

    message = (
        f"{result_color} <b>{normalized_result['name']} - {normalized_result['value']}</b>\n"
        "\n"
        f"Нормы для мужчин: {normalized_result['normsMan']}\n"
        f"Нормы для женщин: {normalized_result['normsWoman']}\n"
        "\n"
        f"<b>Описание</b>: {normalized_result['description']}\n"
        f"{reasons_text}"
        f"{conclusion_text}"
        f"{consult_advice}"
    )

    return message


def strip_html_tags(text):
    return re.sub("<[^<]+?>", "", text)
