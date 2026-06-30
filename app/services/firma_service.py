from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.firma_repository import FirmaRepository
from app.repositories.credito_repository import SolicitudCreditoRepository


class FirmaService:
    def __init__(self, db: Session):
        self.db = db
        self.firma_repo = FirmaRepository(db)
        self.solicitud_repo = SolicitudCreditoRepository(db)

    def registrar_firma(self, solicitud_id: int, firma_base64: str):
        solicitud = self.solicitud_repo.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")

        firma = self.firma_repo.create(
            solicitud_id=solicitud_id,
            firma_base64=firma_base64,
        )
        return firma
