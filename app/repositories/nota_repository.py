from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.nota_solicitud import NotaSolicitud

class NotaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, solicitud_id: int, empleado_id: int, contenido: str) -> NotaSolicitud:
        nota = NotaSolicitud(solicitud_id=solicitud_id, empleado_id=empleado_id, contenido=contenido)
        self.db.add(nota)
        self.db.flush()
        return nota

    def get_by_solicitud_id(self, solicitud_id: int):
        return self.db.query(NotaSolicitud).filter(NotaSolicitud.solicitud_id == solicitud_id).order_by(desc(NotaSolicitud.created_at)).all()
