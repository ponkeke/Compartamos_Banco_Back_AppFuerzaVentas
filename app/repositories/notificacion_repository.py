from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.notificacion import Notificacion


class NotificacionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, cliente_id: int, tipo: str, titulo: str, descripcion: str | None = None) -> Notificacion:
        notif = Notificacion(
            cliente_id=cliente_id,
            tipo=tipo,
            titulo=titulo,
            descripcion=descripcion,
        )
        print("        >>> ANTES DE DB.ADD (notificacion)")
        self.db.add(notif)
        print("        >>> DESPUES DE DB.ADD (notificacion)")
        print("        >>> ANTES DE DB.FLUSH (notificacion)")
        self.db.flush()
        print("        >>> DESPUES DE DB.FLUSH (notificacion)")
        return notif

    def get_by_cliente_id(self, cliente_id: int):
        return (
            self.db.query(Notificacion)
            .filter(Notificacion.cliente_id == cliente_id)
            .order_by(desc(Notificacion.fecha))
            .all()
        )

    def get_by_id(self, notificacion_id: int) -> Notificacion | None:
        return self.db.query(Notificacion).filter(Notificacion.id == notificacion_id).first()

    def marcar_leida(self, notificacion: Notificacion):
        notificacion.leida = True
        self.db.flush()
        return notificacion

    def get_all(self):
        return (
            self.db.query(Notificacion)
            .order_by(desc(Notificacion.fecha))
            .all()
        )
