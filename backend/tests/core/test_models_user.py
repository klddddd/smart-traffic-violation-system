# tests/core/test_models_user.py
from app.models.user import Role, User


def test_create_role_and_user(db):
    role = Role(code="citizen", name="市民")
    db.add(role)
    db.commit()
    user = User(username="u1", password_hash="h", email="u@e.com", role_id=role.id)
    db.add(user)
    db.commit()
    assert user.id is not None
    assert user.role.code == "citizen"
    assert user.status == "active"
