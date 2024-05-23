import base64
import os
import requests
import json

from ai.promt import PROMT

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def send_to_chatgpt_vision(image_paths):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    images_content = []
    for image_path in image_paths:
        with open(image_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode('utf-8')
            images_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}})  

    paload = {
        "model": "gpt-4o",
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": "You are an assistant specialized in analyzing medical images and prompt in JSON format in Russian language. Your response has to be in JSON format only."},
            {"role": "user", "content": [
                {"type": "text", "text": json.dumps(PROMT)},
                *images_content
            ]}
        ],
    }

    response = requests.post(url, headers=headers, json=paload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
