import concurrent.futures
import requests
import traceback


def send_post(url, payload, headers=None):
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Request failed with status code {response.status_code}: {response.text}"
        )


def send_multi_post(url, payloads, headers=None):
    result = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futures = {
            executor.submit(send_post, url, payload, headers): payload
            for payload in payloads
        }
        for future in concurrent.futures.as_completed(futures):
            try:
                result.append(future.result())
            except Exception as e:
                result.append(traceback.format_exc(e))
