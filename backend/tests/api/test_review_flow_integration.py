# tests/api/test_review_flow_integration.py
from app.core.deps import get_notification_provider
from app.core.security import create_access_token
from app.services.notification_provider import FakeNotificationProvider


def test_full_approve_flow_with_vehicle_and_template(
    client, db, citizen_user, reviewer_user, pending_case, reviewer_auth_headers, tmp_path, monkeypatch
):
    monkeypatch.setattr("app.services.storage.settings.MEDIA_STORAGE_DIR", str(tmp_path))
    # 用 Fake 通知 provider，避免打真实 SMTP
    client.app.dependency_overrides[get_notification_provider] = lambda: FakeNotificationProvider()

    from app.models.violation import NotificationTemplate, Vehicle
    db.add(NotificationTemplate(code="violation_notice", subject_template="s:{violation_type}",
                                body_template="b:{plate_no}"))
    db.add(Vehicle(plate_no="粤A12345", owner_id=citizen_user.id, vehicle_type="小汽车"))
    db.commit()

    r = client.post(f"/api/v1/cases/{pending_case.id}/approve", headers=reviewer_auth_headers,
                    json={"plate_no": "粤A12345", "violation_type": "超速", "fine_amount": 200,
                          "points": 6, "review_opinion": "证据清晰"})
    assert r.status_code == 200
    data = r.json()
    assert data["violation_no"].startswith("VIO")
    assert data["notification_status"] == "sent"   # Fake provider + 车主有 email
    assert data["reward_id"] is not None           # citizen 源 → 奖励

    # 案件状态 → notified
    r2 = client.get(f"/api/v1/cases/{pending_case.id}", headers=reviewer_auth_headers)
    assert r2.json()["status"] == "notified"

    # 车主能查到自己的违章
    citizen_token = create_access_token(subject=str(citizen_user.id), role="citizen")
    r3 = client.get(f"/api/v1/owners/{citizen_user.id}/violations",
                    headers={"Authorization": f"Bearer {citizen_token}"})
    assert r3.status_code == 200
    assert r3.json()["total"] == 1
