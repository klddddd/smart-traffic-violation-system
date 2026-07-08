# app/schemas/intake.py
from pydantic import BaseModel


class IntakeResponse(BaseModel):
    case_id: int
    case_no: str
    status: str
    message: str
