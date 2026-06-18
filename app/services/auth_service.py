from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.cuenta_repository import CuentaRepository
from app.repositories.empleado_repository import EmpleadoRepository
from app.repositories.notificacion_repository import NotificacionRepository
from app.core.security import hash_password, verify_password, create_access_token
import random
import string


def _coincide_clave(plain: str, hashed: str) -> bool:
    """Verifica clave con bcrypt; fallback a texto plano para pruebas locales."""
    try:
        if verify_password(plain, hashed):
            return True
    except Exception as e:
        print(f"[AUTH] bcrypt verify exception: {e}")
    # Fallback texto plano (solo pruebas)
    if plain == hashed:
        print("[AUTH] Clave coincide en texto plano (FALLBACK)")
        return True
    return False


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.cliente_repo = ClienteRepository(db)
        self.cuenta_repo = CuentaRepository(db)
        self.empleado_repo = EmpleadoRepository(db)
        self.notificacion_repo = NotificacionRepository(db)

    def _generar_numero_cuenta(self) -> str:
        prefix = "400"
        suffix = "".join(random.choices(string.digits, k=11))
        return f"{prefix}{suffix}"

    def register(self, dni: str, nombres: str, apellidos: str, password: str):
        if len(dni) != 8 or not dni.isdigit():
            raise HTTPException(status_code=400, detail="DNI debe tener 8 dígitos")
        if len(password) < 6:
            raise HTTPException(status_code=400, detail="Password mínimo 6 caracteres")

        existe = self.cliente_repo.get_by_dni(dni)
        if existe:
            raise HTTPException(status_code=400, detail="DNI ya registrado")

        clave_hash = hash_password(password)
        print(f"[AUTH] Register DNI={dni} hash={clave_hash[:20]}...")
        cliente = self.cliente_repo.create(dni, nombres, apellidos, clave_hash)

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
            descripcion="Tu cuenta digital ha sido creada exitosamente.",
        )

        return cliente

    def login_cliente(self, numero_documento: str, password: str):
        print(f"[AUTH] Login cliente DNI={numero_documento}")
        cliente = self.cliente_repo.get_by_dni(numero_documento)
        if not cliente:
            print("[AUTH] Cliente NO encontrado")
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        print(f"[AUTH] Cliente encontrado: id={cliente.id} nombres={cliente.nombres}")
        print(f"[AUTH] Clave en BD: {cliente.clave[:20]}...")

        if not _coincide_clave(password, cliente.clave):
            print("[AUTH] Clave NO coincide")
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        print("[AUTH] Login exitoso")
        access_token = create_access_token({"cliente_id": cliente.id, "dni": cliente.dni, "tipo": "CLIENTE"})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "tipo_usuario": "CLIENTE",
            "cliente": {
                "id": cliente.id,
                "dni": cliente.dni,
                "nombres": cliente.nombres,
                "apellidos": cliente.apellidos,
            },
        }

    def login_empleado(self, codigo_empleado: str, password: str):
        print(f"[AUTH] Login empleado codigo={codigo_empleado}")
        empleado = self.empleado_repo.get_by_codigo(codigo_empleado)
        if not empleado:
            print("[AUTH] Empleado NO encontrado")
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        print(f"[AUTH] Empleado encontrado: id={empleado.id} nombres={empleado.nombres}")
        if not _coincide_clave(password, empleado.password):
            print("[AUTH] Clave NO coincide")
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        if empleado.estado != "ACTIVO":
            print(f"[AUTH] Empleado inactivo: {empleado.estado}")
            raise HTTPException(status_code=403, detail="Empleado inactivo")

        print("[AUTH] Login empleado exitoso")
        access_token = create_access_token({"empleado_id": empleado.id, "codigo": empleado.codigo_empleado, "tipo": "EMPLEADO"})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "tipo_usuario": "EMPLEADO",
            "empleado": {
                "id": empleado.id,
                "codigo_empleado": empleado.codigo_empleado,
                "nombres": empleado.nombres,
                "apellidos": empleado.apellidos,
                "cargo": empleado.cargo,
            },
        }
