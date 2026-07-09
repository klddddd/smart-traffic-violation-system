# app/services/notification_provider.py
import smtplib
from dataclasses import dataclass

from app.core.config import settings


@dataclass
class SendResult:
    status: str  # "sent" | "failed"
    provider_msg_id: str | None = None
    error: str | None = None


class NotificationProvider:
    def send(self, to_email: str, subject: str, body: str) -> SendResult:
        raise NotImplementedError


class EmailSmtpProvider(NotificationProvider):
    def send(self, to_email: str, subject: str, body: str) -> SendResult:
        if not settings.SMTP_HOST or not settings.SMTP_FROM:
            return SendResult("failed", error="smtp_not_configured")
        try:
            msg = (
                f"From: {settings.SMTP_FROM}\r\n"
                f"To: {to_email}\r\n"
                f"Subject: {subject}\r\n\r\n"
                f"{body}"
            )
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as s:
                if settings.SMTP_USER:
                    s.starttls()
                    s.login(settings.SMTP_USER, settings.SMTP_PASSWORD or "")
                s.sendmail(settings.SMTP_FROM, [to_email], msg.encode("utf-8"))
            return SendResult("sent", provider_msg_id="email")
        except Exception as exc:
            return SendResult("failed", error=str(exc))


class FakeNotificationProvider(NotificationProvider):
    def __init__(self) -> None:
        self.sent: list[tuple[str, str, str]] = []

    def send(self, to_email: str, subject: str, body: str) -> SendResult:
        self.sent.append((to_email, subject, body))
        return SendResult("sent", provider_msg_id="fake")
