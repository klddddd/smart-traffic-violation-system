# app/services/image_validate.py
from fastapi import HTTPException

from app.core.config import settings

_MAGIC = [
    (b"\xff\xd8\xff", "image/jpeg"),
    (b"\x89PNG\r\n\x1a\n", "image/png"),
    (b"RIFF", "image/webp"),  # 进一步校验 WEBP 八字
]


def _sniff_mime(data: bytes) -> str | None:
    for magic, mime in _MAGIC:
        if data.startswith(magic):
            if mime == "image/webp" and data[8:12] != b"WEBP":
                return None
            return mime
    return None


def validate_image(data: bytes, filename: str) -> str:
    if len(data) > settings.MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="图片过大")
    mime = _sniff_mime(data)
    if mime is None or mime not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="不支持的图片格式")
    return mime
