from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    dni: str = Field(..., min_length=8, max_length=8)
    nombres: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=6)


# ── Cliente login ──────────────────────────────────────────

class LoginClienteIn(BaseModel):
    numero_documento: str = Field(..., min_length=8, max_length=8)
    password: str


class ClienteDataOut(BaseModel):
    id: int
    dni: str
    nombres: str
    apellidos: str


class LoginClienteResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    tipo_usuario: str = "CLIENTE"
    cliente: ClienteDataOut


# ── Empleado login ─────────────────────────────────────────

class LoginEmpleadoIn(BaseModel):
    codigo_empleado: str = Field(..., min_length=1, max_length=20)
    password: str


class EmpleadoDataOut(BaseModel):
    id: int
    codigo_empleado: str
    nombres: str
    apellidos: str
    cargo: str


class LoginEmpleadoResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    tipo_usuario: str = "EMPLEADO"
    empleado: EmpleadoDataOut
