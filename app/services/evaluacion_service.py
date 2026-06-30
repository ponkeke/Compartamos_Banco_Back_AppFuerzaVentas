from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.evaluacion_repository import EvaluacionRepository
from app.repositories.credito_repository import SolicitudCreditoRepository
from app.repositories.empleado_repository import EmpleadoRepository


class EvaluacionService:
    def __init__(self, db: Session):
        self.db = db
        self.evaluacion_repo = EvaluacionRepository(db)
        self.solicitud_repo = SolicitudCreditoRepository(db)
        self.empleado_repo = EmpleadoRepository(db)

    def pre_evaluar(self, solicitud_id: int, empleado_id: int, resultado: str, capacidad_pago=None, observaciones=None):
        solicitud = self.solicitud_repo.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")

        empleado = self.empleado_repo.get_by_id(empleado_id)
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")

        if solicitud.estado == "PENDIENTE":
            self.solicitud_repo.update_estado(solicitud, "EN_EVALUACION")

        evaluacion = self.evaluacion_repo.create(
            solicitud_id=solicitud_id,
            empleado_id=empleado_id,
            resultado_pre_evaluacion=resultado,
            capacidad_pago=capacidad_pago,
            observaciones=observaciones,
        )
        return evaluacion

    def evaluar_buro(self, solicitud_id: int, empleado_id: int, resultado: str, observaciones=None):
        solicitud = self.solicitud_repo.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")

        empleado = self.empleado_repo.get_by_id(empleado_id)
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")

        evaluacion = self.evaluacion_repo.create(
            solicitud_id=solicitud_id,
            empleado_id=empleado_id,
            resultado_buro=resultado,
            observaciones=observaciones,
        )
        return evaluacion
