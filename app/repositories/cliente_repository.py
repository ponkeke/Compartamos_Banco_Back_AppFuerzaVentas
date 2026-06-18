from sqlalchemy.orm import Session
from app.models.cliente import Cliente


class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_dni(self, dni: str) -> Cliente | None:
        return self.db.query(Cliente).filter(Cliente.dni == dni).first()

    def get_by_id(self, cliente_id: int) -> Cliente | None:
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def create(self, dni: str, nombres: str, apellidos: str, clave: str) -> Cliente:
        cliente = Cliente(dni=dni, nombres=nombres, apellidos=apellidos, clave=clave)
        self.db.add(cliente)
        self.db.flush()
        return cliente
