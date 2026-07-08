# tests/services/test_image_validate.py
import pytest
from fastapi import HTTPException

from app.services.image_validate import validate_image

JPEG = b"\xff\xd8\xff\xe0" + b"\x00" * 100
PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100


def test_validate_jpeg():
    assert validate_image(JPEG, "a.jpg") == "image/jpeg"


def test_validate_png():
    assert validate_image(PNG, "a.png") == "image/png"


def test_validate_rejects_txt():
    with pytest.raises(HTTPException) as exc:
        validate_image(b"hello world", "a.txt")
    assert exc.value.status_code == 400


def test_validate_rejects_oversize():
    big = b"\xff\xd8\xff\xe0" + b"\x00" * (11 * 1024 * 1024)
    with pytest.raises(HTTPException) as exc:
        validate_image(big, "a.jpg")
    assert exc.value.status_code == 400
