from pydantic import BaseModel, Field


class LoginClienteIn(BaseModel):
    numero_documento: str = Field(..., min_length=8, max_length=8)
    password: str


class ClienteDataOut(BaseModel):
    id: int
    dni: str
    nombres: str
    apellidos: str

    class Config:
        from_attributes = True


class LoginClienteResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    tipo_usuario: str = "CLIENTE"
    cliente: ClienteDataOut


class LoginEmpleadoIn(BaseModel):
    codigo_empleado: str = Field(..., min_length=1, max_length=20)
    password: str


class EmpleadoDataOut(BaseModel):
    id: int
    codigo_empleado: str
    nombres: str
    apellidos: str
    cargo: str

    class Config:
        from_attributes = True


class LoginEmpleadoResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    tipo_usuario: str = "EMPLEADO"
    empleado: EmpleadoDataOut
