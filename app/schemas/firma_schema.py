from pydantic import BaseModel, Field
from datetime import datetime


class FirmaRequest(BaseModel):
    solicitud_id: int
    firma_base64: str


class FirmaOut(BaseModel):
    id: int
    solicitud_id: int | None = None
    firma_base64: str | None = None
    fecha_firma: datetime | None = None

    class Config:
        from_attributes = True
