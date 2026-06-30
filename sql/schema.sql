-- Compartamos Banco - Esquema de Base de Datos
-- PostgreSQL

CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    dni VARCHAR(8) UNIQUE NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    clave VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cuentas (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    numero_cuenta VARCHAR(20) UNIQUE NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    moneda VARCHAR(3) NOT NULL DEFAULT 'PEN',
    saldo NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    tea NUMERIC(5, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS contactos (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS transacciones (
    id SERIAL PRIMARY KEY,
    cuenta_id INTEGER NOT NULL REFERENCES cuentas(id) ON DELETE CASCADE,
    tipo VARCHAR(50) NOT NULL,
    descripcion VARCHAR(255),
    monto NUMERIC(12, 2) NOT NULL,
    saldo_resultante NUMERIC(12, 2) NOT NULL,
    fecha TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS solicitudes_credito (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    tipo_credito VARCHAR(50) NOT NULL,
    monto_solicitado NUMERIC(12, 2) NOT NULL,
    numero_cuotas INTEGER NOT NULL,
    motivo VARCHAR(255),
    ingresos_mensuales NUMERIC(12, 2),
    actividad_economica VARCHAR(100),
    tasa_interes NUMERIC(5, 2),
    cuota_estimada NUMERIC(12, 2),
    estado VARCHAR(20) NOT NULL DEFAULT 'PENDIENTE',
    fecha_solicitud TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_evaluacion TIMESTAMP WITH TIME ZONE,
    empleado_evaluador_id INTEGER REFERENCES empleados(id),
    observacion_evaluacion VARCHAR(500)
);

CREATE TABLE IF NOT EXISTS creditos (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    solicitud_id INTEGER NOT NULL REFERENCES solicitudes_credito(id) ON DELETE CASCADE,
    tipo_credito VARCHAR(50) NOT NULL,
    monto_desembolsado NUMERIC(12, 2) NOT NULL,
    saldo_pendiente NUMERIC(12, 2) NOT NULL,
    tasa_interes NUMERIC(5, 2) NOT NULL,
    numero_cuotas INTEGER NOT NULL,
    cuota_actual INTEGER NOT NULL DEFAULT 0,
    estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVO',
    fecha_inicio DATE,
    fecha_fin DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cronograma_cuotas (
    id SERIAL PRIMARY KEY,
    credito_id INTEGER NOT NULL REFERENCES creditos(id) ON DELETE CASCADE,
    numero_cuota INTEGER NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    capital NUMERIC(12, 2) NOT NULL,
    interes NUMERIC(12, 2) NOT NULL,
    seguro NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    monto_total NUMERIC(12, 2) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'PENDIENTE'
);

CREATE TABLE IF NOT EXISTS empleados (
    id SERIAL PRIMARY KEY,
    codigo_empleado VARCHAR(20) UNIQUE NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    cargo VARCHAR(100) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVO',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS notificaciones (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    tipo VARCHAR(50) NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    leida BOOLEAN NOT NULL DEFAULT FALSE,
    fecha TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_clientes_dni ON clientes(dni);
CREATE INDEX IF NOT EXISTS idx_cuentas_cliente ON cuentas(cliente_id);
CREATE INDEX IF NOT EXISTS idx_transacciones_cuenta ON transacciones(cuenta_id);
CREATE INDEX IF NOT EXISTS idx_solicitudes_cliente ON solicitudes_credito(cliente_id);
CREATE INDEX IF NOT EXISTS idx_creditos_cliente ON creditos(cliente_id);
CREATE TABLE IF NOT EXISTS solicitudes_registro_cliente (
    id SERIAL PRIMARY KEY,
    dni VARCHAR(8) NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    celular VARCHAR(15) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'PENDIENTE',
    observacion TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_solicitudes_registro_dni ON solicitudes_registro_cliente(dni);
CREATE INDEX IF NOT EXISTS idx_solicitudes_registro_estado ON solicitudes_registro_cliente(estado);
CREATE INDEX IF NOT EXISTS idx_notificaciones_cliente ON notificaciones(cliente_id);
