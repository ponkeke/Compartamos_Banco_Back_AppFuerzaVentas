from pydantic import BaseModel
from datetime import datetime


class ClienteOut(BaseModel):
    id: int
    dni: str
    nombres: str
    apellidos: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True
