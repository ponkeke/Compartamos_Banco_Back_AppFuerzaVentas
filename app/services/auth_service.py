from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.empleado_repository import EmpleadoRepository
from app.core.security import verify_password, create_access_token


def _coincide_clave(plain: str, hashed: str) -> bool:
    try:
        return verify_password(plain, hashed)
    except Exception as e:
        print(f"[AUTH] bcrypt verify exception: {e}")
        return False


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.cliente_repo = ClienteRepository(db)
        self.empleado_repo = EmpleadoRepository(db)

    def login_cliente(self, numero_documento: str, password: str):
        print(f"[AUTH] Login cliente DNI={numero_documento}")
        cliente = self.cliente_repo.get_by_dni(numero_documento)
        if not cliente:
            print("[AUTH] Cliente NO encontrado")
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        if cliente.estado_registro != "ACTIVO":
            print(f"[AUTH] Cliente estado={cliente.estado_registro}")
            raise HTTPException(status_code=403, detail="Cuenta pendiente de aprobación")

        if not _coincide_clave(password, cliente.clave):
            print("[AUTH] Clave NO coincide")
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

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

        if not _coincide_clave(password, empleado.password):
            print("[AUTH] Clave NO coincide")
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        if empleado.estado != "ACTIVO":
            raise HTTPException(status_code=403, detail="Empleado inactivo")

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
