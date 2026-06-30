from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.documento_credito import DocumentoCredito


class DocumentoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, solicitud_id: int, tipo_documento: str, archivo_url: str) -> DocumentoCredito:
        doc = DocumentoCredito(
            solicitud_id=solicitud_id,
            tipo_documento=tipo_documento,
            archivo_url=archivo_url,
        )
        self.db.add(doc)
        self.db.flush()
        return doc

    def get_by_solicitud_id(self, solicitud_id: int):
        return (
            self.db.query(DocumentoCredito)
            .filter(DocumentoCredito.solicitud_id == solicitud_id)
            .order_by(desc(DocumentoCredito.fecha_subida))
            .all()
        )
