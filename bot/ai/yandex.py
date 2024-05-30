import os
import requests
import json
import traceback
import pytesseract
from PIL import Image

from ai.promt import OBSERVATION_INTERPRETATION_PROMT, CUT_TEXT_PROMT
from utils.multiprocess import send_multi_post
from utils.strings import chunk_text_by_linebreaks
from logger import logger

YANDEX_AI_CATALOG_ID = os.getenv("YANDEX_AI_CATALOG_ID")
YANDEX_AI_KEY_ID = os.getenv("YANDEX_AI_KEY_ID")
YANDEX_AI_API_KEY = os.getenv("YANDEX_AI_API_KEY")

YANDEX_AI_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
YANDEX_AI_HEADERS = {
    "Authorization": f"Api-Key {YANDEX_AI_API_KEY}",
    "Content-Type": "application/json",
}


def get_observation_values(image_paths):
    images_content = ""
    for image_path in image_paths:
        image = Image.open(image_path)
        image_text = pytesseract.image_to_string(image, lang="rus")
        images_content += image_text

    chunked_images_content = chunk_text_by_linebreaks(images_content)
    paload = {
        "modelUri": f"gpt://{YANDEX_AI_CATALOG_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0,
            "maxTokens": 20000,
            "format": "json",
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты асистент специализированный на получении значений анализов из медицинских документов. Твой ответ должен содержать только JSON, основанный на схеме в 'promt'.",
                # "text": "Ты асистент, помогающий убрать лишнюю информацию из документов, которая не относится к медицинским анализам",
            },
            *[
                {"role": "user", "text": images_content}
                for images_content in chunked_images_content
            ],
            {
                "role": "user",
                "text": json.dumps({"promt": OBSERVATION_INTERPRETATION_PROMT}),
            },
        ],
    }

    response = requests.post(YANDEX_AI_URL, headers=YANDEX_AI_HEADERS, json=paload)
    if response.status_code == 200:
        json_data_response = response.json()
        logger.info(
            f"get_observation_values.json_data_response!!!!!!!!!!!!!!!!: {json.dumps(json_data_response)}"
        )
        try:
            return json.loads(json_data_response["choices"][0]["message"]["content"])
        except json.decoder.JSONDecodeError as e:
            logger.error(
                f"get_observation_results.json.JSONDecodeError!!!!!!!!!!!!!!! {traceback.format_exc(e)}"
            )
            return fix_json(
                json_data_response["choices"][0]["message"]["content"],
                traceback.format_exc(e),
            )
    else:
        raise Exception(
            f"Request failed with status code {response.status_code}: {response.text}"
        )


def get_observation_results(image_paths):
    observation_values = get_observation_values(image_paths)

    # paload = {
    #     "model": "gpt-3.5-turbo",
    #     "response_format": {"type": "json_object"},
    #     "messages": [
    #         {
    #             "role": "system",
    #             "content": "You are an assistant specialized in analyzing medical observation data in Russian language. Your response has to be additional information about each observation based on 'response_format' in JSON.",
    #         },
    #         {
    #             "role": "user",
    #             "content": json.dumps(
    #                 {
    #                     **OBSERVATION_INTERPRETATION_PROMT,
    #                     "values": observation_values,
    #                 }
    #             ),
    #         },
    #     ],
    # }

    # response = requests.post(OPEN_AI_URL, headers=OPEN_AI_HEADERS, json=paload)
    # if response.status_code == 200:
    #     json_data_response = response.json()
    #     try:
    #         return json.loads(json_data_response["choices"][0]["message"]["content"])
    #     except json.decoder.JSONDecodeError as e:
    #         logger.error(
    #             f"get_observation_results.json.JSONDecodeError!!!!!!!!!!!!!!! {traceback.format_exc(e)}"
    #         )
    #         return fix_json(
    #             json_data_response["choices"][0]["message"]["content"],
    #             traceback.format_exc(e),
    #         )
    # else:
    #     raise Exception(
    #         f"Request failed with status code {response.status_code}: {response.text}"
    #    )


def fix_json(json_data: str, error_message: str):
    paload = {
        "model": "gpt-3.5-turbo",
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "system",
                "content": "You are an assistant specialized in analyzing JSON and fixing JSON format. Your response has to be fixed JSON.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": json_data,
                    },
                    {
                        "type": "text",
                        "text": error_message,
                    },
                ],
            },
        ],
    }

    response = requests.post(OPEN_AI_URL, headers=OPEN_AI_HEADERS, json=paload)
    if response.status_code == 200:
        json_data_response = response.json()
        try:
            return json.loads(json_data_response["choices"][0]["message"]["content"])
        except json.decoder.JSONDecodeError as e:
            logger.error(
                f"fix_json.json.JSONDecodeError!!!!!!!!!!!!!!! {traceback.format_exc(e)}"
            )
            return fix_json(
                json_data_response["choices"][0]["message"]["content"],
                traceback.format_exc(e),
            )
    else:
        raise Exception(
            f"Request failed with status code {response.status_code}: {response.text}"
        )
