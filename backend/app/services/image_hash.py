# app/services/image_hash.py
import hashlib


def compute_image_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
