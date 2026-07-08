# tests/services/test_image_hash.py
from app.services.image_hash import compute_image_hash


def test_hash_stable():
    assert compute_image_hash(b"abc") == compute_image_hash(b"abc")


def test_hash_differs():
    assert compute_image_hash(b"abc") != compute_image_hash(b"abd")


def test_hash_is_hex():
    h = compute_image_hash(b"abc")
    assert len(h) == 64
    int(h, 16)  # 不抛即合法十六进制
