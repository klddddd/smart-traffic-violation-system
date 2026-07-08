# tests/services/test_storage.py
import os

from app.services.storage import save_media


def test_save_media_writes_file(tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.storage.settings.MEDIA_STORAGE_DIR", str(tmp_path))
    data = b"\xff\xd8\xff\xe0" + b"\x00" * 10
    url, ext = save_media(data, "image/jpeg")
    assert ext == "jpg"
    filename = url.split("/")[-1]
    path = os.path.join(str(tmp_path), filename)
    assert os.path.exists(path)
    with open(path, "rb") as f:
        assert f.read() == data
