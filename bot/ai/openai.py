import os
import requests
import json
import traceback
import pytesseract
import datetime
from PIL import Image

from ai.promt import (
    CUT_TEXT_PROMT,
    OBSERVATION_INTERPRETATION_PROMT,
    OBSEVATION_GET_VAUES_PROMT,
)
from file.utils import normalize_image
from utils.strings import chunk_text_by_linebreaks
from logger import logger

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPEN_AI_URL = "https://api.openai.com/v1/chat/completions"
OPEN_AI_HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
}


def get_observation_values(image_paths):
    json_log_data = {}

    images_content = ""
    for image_path in image_paths:
        image = normalize_image(image_path)
        image_text = pytesseract.image_to_string(image, lang="rus")
        images_content += image_text

    json_log_data["request"] = images_content

    chunked_images_content = chunk_text_by_linebreaks(images_content)

    paload = {
        "model": "gpt-4o",
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "system",
                "content": "You are an assistant specialized in getting observations tests results with numbers from medical documents in Russian language and return the negative results in JSON format based on schema in promt.",
                # "content": "You are an assistant specialized in getting only medical observations data values from medical documents in Russian language.",
            },
            *[
                {"role": "user", "content": images_content}
                for images_content in chunked_images_content
            ],
            # {
            #     "role": "user",
            #     "content": images_content,
            # },
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
            result = json.loads(json_data_response["choices"][0]["message"]["content"])
            json_log_data["response"] = result

            current_dir = os.path.dirname(os.path.abspath(__file__))
            json_log_filename = f"{current_dir}/requests_data/json_log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
            json_log_file = open(json_log_filename, "w")
            json_log_file.write(json.dumps(json_log_data))
            json_log_file.close()

            return result
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
