from sqlalchemy.orm import Session
from app.models.empleado import Empleado


class EmpleadoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_codigo(self, codigo_empleado: str) -> Empleado | None:
        return self.db.query(Empleado).filter(Empleado.codigo_empleado == codigo_empleado).first()

    def get_by_id(self, empleado_id: int) -> Empleado | None:
        return self.db.query(Empleado).filter(Empleado.id == empleado_id).first()
