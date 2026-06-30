from sqlalchemy.orm import Session
from app.models.firma_cliente import FirmaCliente


class FirmaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, solicitud_id: int, firma_base64: str) -> FirmaCliente:
        firma = FirmaCliente(
            solicitud_id=solicitud_id,
            firma_base64=firma_base64,
        )
        self.db.add(firma)
        self.db.flush()
        return firma

    def get_by_solicitud_id(self, solicitud_id: int) -> FirmaCliente | None:
        return (
            self.db.query(FirmaCliente)
            .filter(FirmaCliente.solicitud_id == solicitud_id)
            .first()
        )
