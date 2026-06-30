from sqlalchemy.orm import Session
from app.models.evaluacion_credito import EvaluacionCredito


class EvaluacionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, solicitud_id: int, empleado_id: int, **kwargs) -> EvaluacionCredito:
        evaluacion = EvaluacionCredito(
            solicitud_id=solicitud_id,
            empleado_id=empleado_id,
        )
        for k, v in kwargs.items():
            if v is not None and hasattr(evaluacion, k):
                setattr(evaluacion, k, v)
        self.db.add(evaluacion)
        self.db.flush()
        return evaluacion

    def get_by_solicitud_id(self, solicitud_id: int) -> EvaluacionCredito | None:
        return (
            self.db.query(EvaluacionCredito)
            .filter(EvaluacionCredito.solicitud_id == solicitud_id)
            .first()
        )
