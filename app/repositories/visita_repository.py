from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.visita_campo import VisitaCampo


class VisitaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, solicitud_id: int, empleado_id: int, estado_visita: str, observacion: str | None = None, latitud=None, longitud=None) -> VisitaCampo:
        visita = VisitaCampo(
            solicitud_id=solicitud_id,
            empleado_id=empleado_id,
            estado_visita=estado_visita,
            observacion=observacion,
            latitud=latitud,
            longitud=longitud,
        )
        self.db.add(visita)
        self.db.flush()
        return visita

    def get_by_solicitud_id(self, solicitud_id: int):
        return (
            self.db.query(VisitaCampo)
            .filter(VisitaCampo.solicitud_id == solicitud_id)
            .order_by(desc(VisitaCampo.fecha_visita))
            .all()
        )
