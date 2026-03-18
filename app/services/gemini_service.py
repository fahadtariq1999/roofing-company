import os
from typing import Optional

try:
    import google.generativeai as genai
except Exception:  # pragma: no cover
    genai = None

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
MODEL_NAME = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')

if genai and GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def _fallback_reply(prompt: str) -> str:
    lower = prompt.lower()
    if 'storm' in lower or 'hail' in lower:
        return (
            'Storm and hail damage can often qualify for insurance-supported repairs. '
            'I recommend booking a free inspection so the team can assess the roof and next steps.'
        )
    if 'estimate' in lower or 'cost' in lower or 'price' in lower:
        return (
            'Roofing cost depends on roof size, material, pitch, and damage level. '
            'Share your address and roof type and the team can give you a faster estimate.'
        )
    return (
        'Thanks for reaching out. I can help with roof repair, replacement, storm damage questions, '
        'and booking a free inspection.'
    )


def generate_reply(prompt: str) -> str:
    if not genai or not GEMINI_API_KEY:
        return _fallback_reply(prompt)

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    text: Optional[str] = getattr(response, 'text', None)
    return text or _fallback_reply(prompt)
