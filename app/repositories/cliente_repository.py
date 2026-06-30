from sqlalchemy.orm import Session
from app.models.cliente import Cliente


class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_dni(self, dni: str) -> Cliente | None:
        return self.db.query(Cliente).filter(Cliente.dni == dni).first()

    def get_by_id(self, cliente_id: int) -> Cliente | None:
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def get_all(self):
        return self.db.query(Cliente).order_by(Cliente.id).all()

    def create(self, dni: str, nombres: str, apellidos: str, clave: str, **kwargs) -> Cliente:
        cliente = Cliente(dni=dni, nombres=nombres, apellidos=apellidos, clave=clave)
        for k, v in kwargs.items():
            if v is not None and hasattr(cliente, k):
                setattr(cliente, k, v)
        self.db.add(cliente)
        self.db.flush()
        return cliente

    def get_pendientes(self):
        return self.db.query(Cliente).filter(Cliente.estado_registro == "PENDIENTE").all()

    def update_estado(self, cliente: Cliente, estado: str) -> Cliente:
        cliente.estado_registro = estado
        self.db.flush()
        return cliente
