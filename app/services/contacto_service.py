from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.contacto_repository import ContactoRepository


class ContactoService:
    def __init__(self, db: Session):
        self.db = db
        self.contacto_repo = ContactoRepository(db)

    def listar(self, cliente_id: int):
        return self.contacto_repo.get_by_cliente_id(cliente_id)

    def crear(self, cliente_id: int, nombre: str, apellido: str, telefono: str):
        if not nombre or not apellido or not telefono:
            raise HTTPException(status_code=400, detail="nombre, apellido y telefono son obligatorios")
        return self.contacto_repo.create(cliente_id, nombre, apellido, telefono)

    def eliminar(self, contacto_id: int, cliente_id: int):
        eliminado = self.contacto_repo.delete(contacto_id)
        if not eliminado:
            raise HTTPException(status_code=404, detail="Contacto no encontrado")
        return {"mensaje": "Contacto eliminado"}
