# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.deps import get_current_user
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, MenusOut, TokenResponse, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.query(User).filter(User.username == body.username).first()
    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if user.status != "active":
        raise HTTPException(status_code=403, detail="用户已禁用")
    token = create_access_token(subject=str(user.id), role=user.role.code)
    return TokenResponse(
        access_token=token,
        user=UserOut(id=user.id, username=user.username, role_code=user.role.code),
    )


ROLE_MENUS: dict[str, list[str]] = {
    "citizen": ["citizen_report", "my_violations"],
    "reviewer": ["review_workbench", "violations_query"],
    "admin": ["review_workbench", "violations_query", "system_management", "statistics"],
    "camera": [],
}


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)) -> UserOut:
    return UserOut(id=user.id, username=user.username, role_code=user.role.code)


permissions_router = APIRouter(prefix="/permissions", tags=["permissions"])


@permissions_router.get("/menus", response_model=MenusOut)
def menus(user: User = Depends(get_current_user)) -> MenusOut:
    return MenusOut(menus=ROLE_MENUS.get(user.role.code, []))
