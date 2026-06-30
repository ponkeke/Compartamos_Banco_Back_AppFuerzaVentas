from pydantic import BaseModel, Field
from datetime import datetime


class DocumentoRequest(BaseModel):
    solicitud_id: int
    tipo_documento: str = Field(..., max_length=100)
    archivo_url: str


class DocumentoOut(BaseModel):
    id: int
    solicitud_id: int | None = None
    tipo_documento: str | None = None
    archivo_url: str | None = None
    fecha_subida: datetime | None = None

    class Config:
        from_attributes = True
