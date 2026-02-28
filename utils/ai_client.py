import os
import requests
import json

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")
MODEL = os.getenv("MODEL", "gpt-3.5-turbo")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "500"))

if not OPENAI_API_KEY:
    # Для локальной разработки — через .env
    pass

def call_ai_api(messages):
    """
    messages: list of dicts like [{"role": "system","content":...}, {"role":"user","content":...}, ...]
    Возвращает строку (ответ модели).
    """
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": MAX_TOKENS,
        "temperature": 0.7,
    }

    resp = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if "choices" in data and len(data["choices"]) > 0:
        choice = data["choices"][0]
        # OpenAI chat response
        if "message" in choice and "content" in choice["message"]:
            return choice["message"]["content"].strip()
        if "text" in choice:
            return choice["text"].strip()

    return json.dumps(data, ensure_ascii=False, indent=2)
