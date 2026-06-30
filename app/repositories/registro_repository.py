from sqlalchemy.orm import Session
from app.models.solicitud_registro import SolicitudRegistroCliente


class RegistroRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, dni: str, nombres: str, apellidos: str, celular: str,
               correo: str, password_hash: str) -> SolicitudRegistroCliente:
        solicitud = SolicitudRegistroCliente(
            dni=dni, nombres=nombres, apellidos=apellidos,
            celular=celular, correo=correo, password_hash=password_hash,
            estado="PENDIENTE",
        )
        self.db.add(solicitud)
        self.db.flush()
        return solicitud

    def get_by_id(self, solicitud_id: int) -> SolicitudRegistroCliente | None:
        return self.db.query(SolicitudRegistroCliente).filter(
            SolicitudRegistroCliente.id == solicitud_id
        ).first()

    def get_all(self):
        return self.db.query(SolicitudRegistroCliente).order_by(
            SolicitudRegistroCliente.created_at.desc()
        ).all()

    def get_pendientes(self):
        return self.db.query(SolicitudRegistroCliente).filter(
            SolicitudRegistroCliente.estado == "PENDIENTE"
        ).order_by(SolicitudRegistroCliente.created_at.desc()).all()

    def aprobar(self, solicitud: SolicitudRegistroCliente):
        solicitud.estado = "APROBADO"
        self.db.flush()
        return solicitud

    def rechazar(self, solicitud: SolicitudRegistroCliente, observacion: str):
        solicitud.estado = "RECHAZADO"
        solicitud.observacion = observacion
        self.db.flush()
        return solicitud
