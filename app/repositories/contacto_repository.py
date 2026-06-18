from sqlalchemy.orm import Session
from app.models.contacto import Contacto


class ContactoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_cliente_id(self, cliente_id: int):
        return self.db.query(Contacto).filter(Contacto.cliente_id == cliente_id).all()

    def create(self, cliente_id: int, nombre: str, apellido: str, telefono: str) -> Contacto:
        contacto = Contacto(cliente_id=cliente_id, nombre=nombre, apellido=apellido, telefono=telefono)
        self.db.add(contacto)
        self.db.flush()
        return contacto

    def get_by_id(self, contacto_id: int) -> Contacto | None:
        return self.db.query(Contacto).filter(Contacto.id == contacto_id).first()

    def delete(self, contacto: Contacto):
        self.db.delete(contacto)
        self.db.flush()
