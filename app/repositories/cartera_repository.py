from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.cartera_asignacion import CarteraAsignacion

class CarteraRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_empleado_id(self, empleado_id: int):
        return self.db.query(CarteraAsignacion).filter(CarteraAsignacion.empleado_id == empleado_id).order_by(desc(CarteraAsignacion.score_prioridad)).all()

    def get_by_id(self, cartera_id: int) -> CarteraAsignacion | None:
        return self.db.query(CarteraAsignacion).filter(CarteraAsignacion.id == cartera_id).first()

    def registrar_visita(self, cartera: CarteraAsignacion, resultado: str, observacion: str | None = None, lat=None, lng=None):
        cartera.estado_visita = resultado
        if observacion:
            cartera.observacion = observacion
        if lat is not None:
            cartera.latitud = lat
        if lng is not None:
            cartera.longitud = lng
        from datetime import datetime, timezone
        cartera.fecha_visita = datetime.now(timezone.utc)
        self.db.flush()
        return cartera

    def create(self, solicitud_id: int, empleado_id: int, **kwargs) -> CarteraAsignacion:
        item = CarteraAsignacion(solicitud_id=solicitud_id, empleado_id=empleado_id)
        for k, v in kwargs.items():
            if v is not None and hasattr(item, k):
                setattr(item, k, v)
        self.db.add(item)
        self.db.flush()
        return item
