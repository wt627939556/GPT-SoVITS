import re

_TAG_PATTERN = re.compile(r"\[/?tts:text\]\]?")


def sanitize_text(text: str) -> str:
    return _TAG_PATTERN.sub("", text)
