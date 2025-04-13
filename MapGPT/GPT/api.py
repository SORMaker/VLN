import requests
import base64
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

# 第三方API的URL
THIRD_PARTY_API_URL = "https://try-chatapi.com/v1/chat/completions"
# 第三方API的密钥
THIRD_PARTY_API_KEY = "sk-hoyFfLRVTRc5d2kIID3LaNGeuq4xu6wpxwqSeg3LxuxWTEVu"

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {THIRD_PARTY_API_KEY}"
    }
    response = requests.post(THIRD_PARTY_API_URL, headers=headers, json=kwargs)
    response.raise_for_status()  
    return response.json()

def gpt_infer(system, text, image_list, model="gpt-4-vision-preview", max_tokens=600, response_format=None):
    user_content = []
    for i, image in enumerate(image_list):
        if image is not None:
            user_content.append(
                {
                    "type": "text",
                    "text": f"Image {i}:"
                },
            )

            with open(image, "rb") as image_file:
                image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

            image_message = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}",
                    "detail": "low"
                }
            }
            user_content.append(image_message)

    user_content.append(
        {
            "type": "text",
            "text": text
        }
    )

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_content}
    ]

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0,
        "max_tokens": max_tokens
    }

    if response_format:
        payload["response_format"] = response_format

    result = completion_with_backoff(**payload)
    answer = result["choices"][0]["message"]["content"]
    tokens = result.get("usage", {})

    return answer, tokens