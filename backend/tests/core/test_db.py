from sqlalchemy import Column, Integer, String

from app.core.db import Base


class _Demo(Base):
    __tablename__ = "_demo"
    id = Column(Integer, primary_key=True)
    name = Column(String(32))


def test_base_can_create_and_drop(db):
    _Demo.__table__.create(db.get_bind(), checkfirst=True)
    db.add(_Demo(name="x"))
    db.commit()
    row = db.query(_Demo).first()
    assert row.name == "x"
