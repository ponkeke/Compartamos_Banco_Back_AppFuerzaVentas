from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.visita_repository import VisitaRepository
from app.repositories.credito_repository import SolicitudCreditoRepository
from app.repositories.empleado_repository import EmpleadoRepository


class VisitaService:
    def __init__(self, db: Session):
        self.db = db
        self.visita_repo = VisitaRepository(db)
        self.solicitud_repo = SolicitudCreditoRepository(db)
        self.empleado_repo = EmpleadoRepository(db)

    def registrar_visita(self, solicitud_id: int, empleado_id: int, estado_visita: str, observacion: str | None = None, latitud=None, longitud=None):
        solicitud = self.solicitud_repo.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")

        empleado = self.empleado_repo.get_by_id(empleado_id)
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")

        visita = self.visita_repo.create(
            solicitud_id=solicitud_id,
            empleado_id=empleado_id,
            estado_visita=estado_visita,
            observacion=observacion,
            latitud=latitud,
            longitud=longitud,
        )
        return visita
