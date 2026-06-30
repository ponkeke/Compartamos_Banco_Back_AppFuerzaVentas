-- Migration 002: Missing tables and FK constraints
-- Compartamos Banco

-- 1. Notas de solicitud
CREATE TABLE IF NOT EXISTS notas_solicitud (
    id SERIAL PRIMARY KEY,
    solicitud_id INTEGER NOT NULL REFERENCES solicitudes_credito(id) ON DELETE CASCADE,
    empleado_id INTEGER NOT NULL REFERENCES empleados(id) ON DELETE CASCADE,
    contenido TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Cartera de asignaciones
CREATE TABLE IF NOT EXISTS cartera_asignaciones (
    id SERIAL PRIMARY KEY,
    solicitud_id INTEGER NOT NULL REFERENCES solicitudes_credito(id) ON DELETE CASCADE,
    empleado_id INTEGER NOT NULL REFERENCES empleados(id) ON DELETE CASCADE,
    estado_visita VARCHAR(20) NOT NULL DEFAULT 'PENDIENTE',
    tipo_gestion VARCHAR(50),
    prioridad VARCHAR(10),
    score_prioridad INTEGER DEFAULT 0,
    monto_credito NUMERIC(12,2),
    fecha_asignacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_visita TIMESTAMP WITH TIME ZONE,
    observacion VARCHAR(500),
    latitud NUMERIC(10,7),
    longitud NUMERIC(10,7)
);

-- 3. Add missing FK constraints to existing tables
ALTER TABLE documentos_credito ADD CONSTRAINT fk_documentos_solicitud
    FOREIGN KEY (solicitud_id) REFERENCES solicitudes_credito(id) ON DELETE CASCADE
    NOT VALID;

ALTER TABLE evaluaciones_credito ADD CONSTRAINT fk_evaluaciones_solicitud
    FOREIGN KEY (solicitud_id) REFERENCES solicitudes_credito(id) ON DELETE CASCADE
    NOT VALID;

ALTER TABLE evaluaciones_credito ADD CONSTRAINT fk_evaluaciones_empleado
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE SET NULL
    NOT VALID;

ALTER TABLE firmas_cliente ADD CONSTRAINT fk_firmas_solicitud
    FOREIGN KEY (solicitud_id) REFERENCES solicitudes_credito(id) ON DELETE CASCADE
    NOT VALID;

ALTER TABLE visitas_campo ADD CONSTRAINT fk_visitas_solicitud
    FOREIGN KEY (solicitud_id) REFERENCES solicitudes_credito(id) ON DELETE CASCADE
    NOT VALID;

ALTER TABLE visitas_campo ADD CONSTRAINT fk_visitas_empleado
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE SET NULL
    NOT VALID;

-- 4. Fix timestamp timezone inconsistencies
ALTER TABLE documentos_credito ALTER COLUMN fecha_subida TYPE TIMESTAMP WITH TIME ZONE USING fecha_subida AT TIME ZONE 'UTC';
ALTER TABLE evaluaciones_credito ALTER COLUMN fecha_evaluacion TYPE TIMESTAMP WITH TIME ZONE USING fecha_evaluacion AT TIME ZONE 'UTC';
ALTER TABLE firmas_cliente ALTER COLUMN fecha_firma TYPE TIMESTAMP WITH TIME ZONE USING fecha_firma AT TIME ZONE 'UTC';
ALTER TABLE visitas_campo ALTER COLUMN fecha_visita TYPE TIMESTAMP WITH TIME ZONE USING fecha_visita AT TIME ZONE 'UTC';

-- 5. Reindex for new tables
CREATE INDEX IF NOT EXISTS idx_notas_solicitud_id ON notas_solicitud(solicitud_id);
CREATE INDEX IF NOT EXISTS idx_cartera_empleado ON cartera_asignaciones(empleado_id);
CREATE INDEX IF NOT EXISTS idx_cartera_solicitud ON cartera_asignaciones(solicitud_id);
