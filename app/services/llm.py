import requests

from app.core.config import API_KEY, BASE_URL


class LLMError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


def _extract_text(data) -> str | None:
    if isinstance(data, str):
        return data
    if not isinstance(data, dict):
        return None
    choices = data.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0]
        message = first.get("message")
        if isinstance(message, dict) and message.get("content"):
            return message["content"]
        if first.get("text"):
            return first["text"]
    for key in ("text", "content", "response", "answer", "output", "completion"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return None


def generate_response(prompt: str) -> str:
    try:
        response = requests.post(
            f"{BASE_URL}/v1/completions",
            headers={"X-Student-Key": API_KEY, "Content-Type": "application/json"},
            json={
                "model": "gpt-5",
                "prompt": prompt,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 1,
                "max_tokens": 300,
            },
            timeout=60,
        )
    except requests.Timeout:
        raise LLMError(504, "El backend del curso tardó demasiado")
    except requests.RequestException:
        raise LLMError(502, "No se pudo conectar con el backend del curso")

    if not response.ok:
        raise LLMError(response.status_code, response.text[:500])

    text = _extract_text(response.json())
    if not text:
        raise LLMError(502, "El backend no devolvió texto")
    return text
