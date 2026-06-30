from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.registro_repository import RegistroRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.cuenta_repository import CuentaRepository
from app.repositories.notificacion_repository import NotificacionRepository
from app.core.security import hash_password
import random
import string


class RegistroService:
    def __init__(self, db: Session):
        self.db = db
        self.registro_repo = RegistroRepository(db)
        self.cliente_repo = ClienteRepository(db)
        self.cuenta_repo = CuentaRepository(db)
        self.notificacion_repo = NotificacionRepository(db)

    def _generar_numero_cuenta(self) -> str:
        prefix = "400"
        suffix = "".join(random.choices(string.digits, k=11))
        return f"{prefix}{suffix}"

    def solicitar(self, dni: str, nombres: str, apellidos: str,
                  celular: str, correo: str, password: str):
        if len(dni) != 8 or not dni.isdigit():
            raise HTTPException(status_code=400, detail="DNI debe tener 8 dígitos")
        if len(password) < 6:
            raise HTTPException(status_code=400, detail="Password mínimo 6 caracteres")

        existe = self.cliente_repo.get_by_dni(dni)
        if existe:
            raise HTTPException(status_code=400, detail="DNI ya registrado como cliente")

        existente = self.registro_repo.create(
            dni=dni, nombres=nombres, apellidos=apellidos,
            celular=celular, correo=correo,
            password_hash=hash_password(password),
        )
        return existente

    def obtener(self, solicitud_id: int):
        solicitud = self.registro_repo.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        return solicitud

    def listar(self):
        return self.registro_repo.get_all()

    def aprobar(self, solicitud_id: int):
        solicitud = self.registro_repo.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        if solicitud.estado != "PENDIENTE":
            raise HTTPException(status_code=400, detail=f"Solicitud ya {solicitud.estado}")

        existe = self.cliente_repo.get_by_dni(solicitud.dni)
        if existe:
            raise HTTPException(status_code=400, detail="DNI ya registrado como cliente")

        cliente = self.cliente_repo.create(
            dni=solicitud.dni, nombres=solicitud.nombres,
            apellidos=solicitud.apellidos, clave=solicitud.password_hash,
            estado_registro="ACTIVO",
        )

        numero_cuenta = self._generar_numero_cuenta()
        self.cuenta_repo.create(
            cliente_id=cliente.id,
            numero_cuenta=numero_cuenta,
            tipo="Cuenta Digital Soles",
            moneda="PEN",
            saldo=0.00,
            tea=4.00,
        )

        self.notificacion_repo.create(
            cliente_id=cliente.id,
            tipo="BIENVENIDA",
            titulo="¡Bienvenido a Compartamos Banco!",
            descripcion="Tu solicitud de registro fue aprobada. Ya puedes iniciar sesión.",
        )

        self.registro_repo.aprobar(solicitud)
        return solicitud

    def rechazar(self, solicitud_id: int, observacion: str):
        solicitud = self.registro_repo.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        if solicitud.estado != "PENDIENTE":
            raise HTTPException(status_code=400, detail=f"Solicitud ya {solicitud.estado}")

        self.registro_repo.rechazar(solicitud, observacion)
        return solicitud
