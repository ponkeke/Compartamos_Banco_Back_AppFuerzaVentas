from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.documento_repository import DocumentoRepository
from app.repositories.credito_repository import SolicitudCreditoRepository


class DocumentoService:
    def __init__(self, db: Session):
        self.db = db
        self.documento_repo = DocumentoRepository(db)
        self.solicitud_repo = SolicitudCreditoRepository(db)

    def subir_documento(self, solicitud_id: int, tipo_documento: str, archivo_url: str):
        solicitud = self.solicitud_repo.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")

        doc = self.documento_repo.create(
            solicitud_id=solicitud_id,
            tipo_documento=tipo_documento,
            archivo_url=archivo_url,
        )
        return doc
