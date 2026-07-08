# app/services/storage.py
import os
import uuid

from app.core.config import settings

_MIME_EXT = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}


def save_media(data: bytes, mime: str) -> tuple[str, str]:
    os.makedirs(settings.MEDIA_STORAGE_DIR, exist_ok=True)
    ext = _MIME_EXT.get(mime, "bin")
    filename = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(settings.MEDIA_STORAGE_DIR, filename)
    with open(path, "wb") as f:
        f.write(data)
    return f"/media/{filename}", ext
