# backend/seed_data.py
"""运行时演示 seed：通知模板 + 车辆/车主。运行：uv run python -m seed_data"""
from app.core.db import SessionLocal
from app.models.user import Role, User
from app.models.violation import NotificationTemplate, Vehicle
from app.core.security import hash_password


def run() -> None:
    db = SessionLocal()
    try:
        if not db.query(NotificationTemplate).filter_by(code="violation_notice").first():
            db.add(NotificationTemplate(
                code="violation_notice", channel="email",
                subject_template="【交通违章通知】{violation_type}",
                body_template=("车牌 {plate_no} 于 {occurred_at} 在 {location_text} 发生 {violation_type}，"
                               "罚款 {fine_amount} 元，扣 {points} 分。违章编号 {violation_no}。"),
            ))
        role = db.query(Role).filter_by(code="citizen").first()
        if role and not db.query(User).filter_by(username="owner1").first():
            owner = User(username="owner1", password_hash=hash_password("pass1234"),
                         email="owner1@example.com", role_id=role.id)
            db.add(owner); db.flush()
            db.add(Vehicle(plate_no="粤A12345", owner_id=owner.id, vehicle_type="小汽车", color="白"))
            db.add(Vehicle(plate_no="粤B67890", owner_id=owner.id, vehicle_type="小汽车", color="黑"))
        db.commit()
        print("seed done")
    finally:
        db.close()


if __name__ == "__main__":
    run()
