"""
Lightweight AI abstraction for Kistie Store.
Supports OpenAI-compatible endpoints and Google Gemini via direct HTTP (no extra packages needed).
Set AI_PROVIDER='openai' or 'gemini' in settings / .env.
"""
import logging
from typing import Optional

import requests as _http
from django.conf import settings

logger = logging.getLogger(__name__)

_OPENAI_URL = 'https://api.openai.com/v1/chat/completions'
_GEMINI_URL_TPL = (
    'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}'
)
_GEMINI_DEFAULT_MODEL = 'gemini-2.0-flash'

# Hard cap per call to keep latency + cost low.
_MAX_TOKENS = 512
_TIMEOUT = 20  # seconds


def _call_openai(messages: list[dict], max_tokens: int = _MAX_TOKENS) -> Optional[str]:
    key = getattr(settings, 'OPENAI_API_KEY', '')
    if not key:
        return None
    model = getattr(settings, 'OPENAI_MODEL', 'gpt-4o-mini')
    try:
        resp = _http.post(
            _OPENAI_URL,
            headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
            json={'model': model, 'messages': messages, 'max_tokens': max_tokens},
            timeout=_TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        return data['choices'][0]['message']['content'].strip()
    except Exception as exc:
        logger.warning('OpenAI call failed: %s', exc)
        return None


def _call_gemini(messages: list[dict], max_tokens: int = _MAX_TOKENS) -> Optional[str]:
    key = getattr(settings, 'GEMINI_API_KEY', '')
    if not key:
        return None
    model = getattr(settings, 'GEMINI_MODEL', _GEMINI_DEFAULT_MODEL)
    url = _GEMINI_URL_TPL.format(model=model, key=key)

    # Convert OpenAI-style messages to Gemini contents format.
    # Gemini uses 'user'/'model' roles; system prompt is prepended to first user turn.
    contents = []
    system_text = ''
    for msg in messages:
        role = msg.get('role', 'user')
        text = msg.get('content', '')
        if role == 'system':
            system_text = text
        elif role == 'user':
            combined = f"{system_text}\n\n{text}".strip() if system_text else text
            contents.append({'role': 'user', 'parts': [{'text': combined}]})
            system_text = ''  # only prepend once
        elif role == 'assistant':
            contents.append({'role': 'model', 'parts': [{'text': text}]})

    if not contents:
        return None

    try:
        resp = _http.post(
            url,
            json={
                'contents': contents,
                'generationConfig': {'maxOutputTokens': max_tokens},
            },
            timeout=_TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        return data['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception as exc:
        logger.warning('Gemini call failed: %s', exc)
        return None


def chat_complete(messages: list[dict], max_tokens: int = _MAX_TOKENS) -> Optional[str]:
    """Call whichever provider is configured. Falls back to the other if primary fails."""
    provider = getattr(settings, 'AI_PROVIDER', 'openai').lower()
    if provider == 'gemini':
        result = _call_gemini(messages, max_tokens)
        if result is None:
            result = _call_openai(messages, max_tokens)
    else:
        result = _call_openai(messages, max_tokens)
        if result is None:
            result = _call_gemini(messages, max_tokens)
    return result


def classify_inquiry(subject: str, message: str) -> str:
    """Return one of: bulk_order | delivery | complaint | general."""
    prompt = (
        "Classify this customer inquiry into exactly ONE of these categories: "
        "bulk_order, delivery, complaint, general.\n"
        "Reply with only the category word, nothing else.\n\n"
        f"Subject: {subject}\nMessage: {message[:400]}"
    )
    result = chat_complete(
        [{'role': 'user', 'content': prompt}],
        max_tokens=10,
    )
    if result:
        tag = result.strip().lower().split()[0]
        if tag in ('bulk_order', 'delivery', 'complaint', 'general'):
            return tag
    return 'general'


def analyze_sentiment(text: str) -> str:
    """Return one of: positive | negative | neutral."""
    if not text.strip():
        return 'neutral'
    prompt = (
        "Classify the sentiment of this product review as exactly ONE of: "
        "positive, negative, neutral.\n"
        "Reply with only the sentiment word.\n\n"
        f"Review: {text[:500]}"
    )
    result = chat_complete(
        [{'role': 'user', 'content': prompt}],
        max_tokens=5,
    )
    if result:
        tag = result.strip().lower().split()[0]
        if tag in ('positive', 'negative', 'neutral'):
            return tag
    return 'neutral'


def generate_product_description(name: str, category: str, color: str) -> dict:
    """
    Generate an English description and Luganda translation.
    Returns {'description_en': '...', 'description_lg': '...'}.
    """
    prompt = (
        "You are a copywriter for Kistie Store, a Ugandan fashion boutique in Kampala. "
        "Write a punchy 2-3 sentence product description in English, then translate it into Luganda.\n\n"
        f"Product name: {name}\nCategory: {category}\nColor/material: {color or 'not specified'}\n\n"
        "Format your reply EXACTLY as:\n"
        "EN: <English description>\n"
        "LG: <Luganda translation>"
    )
    result = chat_complete(
        [{'role': 'user', 'content': prompt}],
        max_tokens=300,
    )
    en, lg = '', ''
    if result:
        for line in result.splitlines():
            if line.startswith('EN:'):
                en = line[3:].strip()
            elif line.startswith('LG:'):
                lg = line[3:].strip()
    return {'description_en': en, 'description_lg': lg}


# ---------------------------------------------------------------------------
# Size recommendation (rule-based — no AI needed, no extra packages)
# EU women's standard measurements (bust / waist / hips in cm)
# ---------------------------------------------------------------------------
_EU_SIZE_TABLE = [
    ('32', 72, 56, 80),
    ('34', 76, 60, 84),
    ('36', 80, 64, 88),
    ('38', 84, 68, 92),
    ('40', 88, 72, 96),
    ('42', 92, 76, 100),
    ('44', 96, 80, 104),
    ('46', 100, 84, 108),
    ('48', 104, 88, 112),
    ('50', 108, 92, 116),
    ('52', 112, 96, 120),
    ('54', 116, 100, 124),
]


def recommend_size(bust: float, waist: float, hips: float) -> dict:
    """
    Map body measurements (cm) to the best-matching EU size.
    Returns {'size': '38', 'note': '...'}.
    """
    best_size = '38'
    best_score = float('inf')

    for size, ref_bust, ref_waist, ref_hips in _EU_SIZE_TABLE:
        score = abs(bust - ref_bust) + abs(waist - ref_waist) + abs(hips - ref_hips)
        if score < best_score:
            best_score = score
            best_size = size

    note = (
        f"Based on bust {bust} cm, waist {waist} cm, hips {hips} cm — "
        f"EU {best_size} is your closest match. Try one size up if you prefer a relaxed fit."
    )
    return {'size': best_size, 'note': note}
