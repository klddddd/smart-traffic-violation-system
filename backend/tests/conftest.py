import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.core.db import Base, get_db
from app.main import app

TEST_DB_URL = "sqlite:///:memory:"
# StaticPool: in-memory SQLite is per-connection; FastAPI's TestClient runs the
# ASGI app in a worker thread, so we must share a single connection across
# threads or tables created in the main thread won't be visible to requests.
test_engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)


@pytest.fixture()
def db() -> Session:
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def client(db: Session) -> TestClient:
    def _override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


from app.core.security import create_access_token, hash_password
from app.models.user import Role, User


@pytest.fixture()
def seeded_roles(db: Session) -> dict[str, Role]:
    mapping = {
        "citizen": "市民",
        "reviewer": "审核员",
        "admin": "管理员",
        "camera": "摄像头",
    }
    result = {}
    for code, name in mapping.items():
        role = Role(code=code, name=name)
        db.add(role)
        result[code] = role
    db.commit()
    return result


@pytest.fixture()
def citizen_user(db: Session, seeded_roles) -> User:
    user = User(
        username="citizen1",
        password_hash=hash_password("pass1234"),
        email="citizen@example.com",
        role_id=seeded_roles["citizen"].id,
    )
    db.add(user)
    db.commit()
    return user


@pytest.fixture()
def citizen_token(citizen_user: User) -> str:
    return create_access_token(subject=str(citizen_user.id), role="citizen")


@pytest.fixture()
def auth_headers(citizen_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {citizen_token}"}


from app.models.intake import CameraApiKey, CameraDevice


@pytest.fixture()
def camera_device(db: Session) -> CameraDevice:
    dev = CameraDevice(device_code="CAM01", location_text="路口B")
    db.add(dev)
    db.commit()
    return dev


@pytest.fixture()
def camera_key(db: Session, camera_device: CameraDevice) -> tuple[str, CameraApiKey]:
    raw = "cam-key-123"
    key = CameraApiKey(camera_device_id=camera_device.id, key_hash=hash_password(raw))
    db.add(key)
    db.commit()
    return raw, key
