import os
import requests
import json
import traceback
import pytesseract
from PIL import Image

from ai.promt import (
    CUT_TEXT_PROMT,
    OBSERVATION_INTERPRETATION_PROMT,
    OBSEVATION_GET_VAUES_PROMT,
)
from utils.strings import chunk_text_by_linebreaks
from logger import logger

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPEN_AI_URL = "https://api.openai.com/v1/chat/completions"
OPEN_AI_HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
}


def get_observation_values(image_paths):
    images_content = ""
    for image_path in image_paths:
        image = Image.open(image_path)
        image_text = pytesseract.image_to_string(image, lang="rus")
        images_content += image_text

    # chunked_images_content = chunk_text_by_linebreaks(images_content)

    paload = {
        "model": "gpt-4o",
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "system",
                "content": "You are an assistant specialized in getting observations tests values from medical documents data in Russian language and return the results in JSON format. Don't get categories, only tests values of medical obsevations and return results with negative 'conclusion_code' only.",
                # "content": "You are an assistant specialized in getting only medical observations data values from medical documents in Russian language.",
            },
            # *[
            #     {"role": "user", "content": images_content}
            #     for images_content in chunked_images_content
            # ],
            {
                "role": "user",
                "content": images_content,
            },
            {
                "role": "user",
                "content": json.dumps(OBSERVATION_INTERPRETATION_PROMT),
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
    logger.info(f"observation_values!!!!!!!!!!!!!!!!!!!!!!!!!!!!: {observation_values}")

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
