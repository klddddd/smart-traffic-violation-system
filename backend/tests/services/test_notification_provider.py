# tests/services/test_notification_provider.py
from app.services.notification_provider import (
    EmailSmtpProvider, FakeNotificationProvider, SendResult,
)


def test_fake_provider_records_send():
    p = FakeNotificationProvider()
    r = p.send("o@e.com", "主题", "正文")
    assert isinstance(r, SendResult)
    assert r.status == "sent"
    assert p.sent == [("o@e.com", "主题", "正文")]


def test_email_smtp_provider_missing_config_returns_failed(monkeypatch):
    from app.services import notification_provider as mod
    monkeypatch.setattr(mod.settings, "SMTP_HOST", None)
    p = EmailSmtpProvider()
    r = p.send("o@e.com", "s", "b")
    assert r.status == "failed"
    assert r.error  # 有错误信息
