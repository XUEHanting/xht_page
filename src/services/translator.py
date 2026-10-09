import json
import os
import re

import requests

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "deepseek/deepseek-v4.1-flash"

SUPPORTED_LANGUAGES = {
    "zh": "Chinese",
    "en": "English",
}


class TranslationError(Exception):
    """Raised when translation fails."""


def translate_note(title: str, content: str, target_lang: str) -> dict:
    """Translate note title and content to the target language via OpenRouter."""
    title = title if isinstance(title, str) else ""
    content = content if isinstance(content, str) else ""

    if not title.strip() and not content.strip():
        raise TranslationError("Title or content is required")

    if target_lang not in SUPPORTED_LANGUAGES:
        raise TranslationError(
            f"Unsupported language '{target_lang}'. Use one of: {', '.join(SUPPORTED_LANGUAGES)}"
        )

    language_name = SUPPORTED_LANGUAGES[target_lang]
    system_prompt = (
        f"You are a professional translator. Translate the note title and content into "
        f"{language_name}. Preserve the original meaning, tone, and formatting. "
        f'Return ONLY a JSON object with keys "title" and "content". '
        f"Do not wrap the JSON in markdown code fences."
    )
    user_prompt = json.dumps({"title": title, "content": content}, ensure_ascii=False)

    raw = _call_openrouter(system_prompt, user_prompt)
    return _parse_note_translation(raw, title, content)


def translate_text(content: str, target_lang: str) -> str:
    """Translate a single text string to the target language via OpenRouter."""
    if not content or not content.strip():
        raise TranslationError("Content is empty")

    if target_lang not in SUPPORTED_LANGUAGES:
        raise TranslationError(
            f"Unsupported language '{target_lang}'. Use one of: {', '.join(SUPPORTED_LANGUAGES)}"
        )

    language_name = SUPPORTED_LANGUAGES[target_lang]
    system_prompt = (
        f"You are a professional translator. Translate the user's text into "
        f"{language_name}. Preserve the original meaning, tone, and formatting. "
        f"Return only the translated text with no explanations or extra notes."
    )
    return _call_openrouter(system_prompt, content)


def _call_openrouter(system_prompt: str, user_content: str) -> str:
    api_key = (os.getenv("OPENROUTER_API_KEY") or "").strip()
    if (
        not api_key
        or api_key in {"sk-or-v1-your-key-here", "your_openrouter_api_key_here"}
    ):
        raise TranslationError(
            "OPENROUTER_API_KEY is not configured. Copy .env.example to .env and set your key."
        )

    model = (os.getenv("OPENROUTER_MODEL") or DEFAULT_MODEL).strip() or DEFAULT_MODEL

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5001",
        "X-Title": "NoteTaker",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "temperature": 0.2,
    }

    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=60,
        )
    except requests.RequestException as exc:
        raise TranslationError(f"Failed to reach OpenRouter: {exc}") from exc

    if response.status_code != 200:
        detail = _extract_error_message(response)
        raise TranslationError(f"OpenRouter API error ({response.status_code}): {detail}")

    data = response.json()
    try:
        translated = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise TranslationError("Unexpected response format from OpenRouter") from exc

    if not translated or not str(translated).strip():
        raise TranslationError("Translation result is empty")

    return str(translated).strip()


def _parse_note_translation(raw: str, original_title: str, original_content: str) -> dict:
    cleaned = raw.strip()
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
    if fence_match:
        cleaned = fence_match.group(1).strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise TranslationError("Unexpected translation response format") from exc

    if not isinstance(data, dict):
        raise TranslationError("Unexpected translation response format")

    translated_title = data.get("title", original_title)
    translated_content = data.get("content", original_content)

    if not isinstance(translated_title, str):
        translated_title = str(translated_title) if translated_title is not None else original_title
    if not isinstance(translated_content, str):
        translated_content = (
            str(translated_content) if translated_content is not None else original_content
        )

    return {
        "title": translated_title.strip(),
        "content": translated_content.strip(),
    }


def _extract_error_message(response: requests.Response) -> str:
    try:
        data = response.json()
        if isinstance(data, dict):
            error = data.get("error")
            if isinstance(error, dict):
                return error.get("message") or str(error)
            if error:
                return str(error)
            return str(data)
    except ValueError:
        pass
    return response.text[:300] or "Unknown error"
