-- Compartamos Banco - Datos de prueba
-- Password: 123456 (hasheado con bcrypt)

INSERT INTO clientes (dni, nombres, apellidos, clave)
VALUES (
    '75280128',
    'TANIA',
    'AUQUI HUINCHO',
    '$2b$12$.fcfYhi/ZoRGMyEvutTtWu.9g.UzyqqG8ar4eH4CNd16dz0VwsaC.'
);

-- Cuenta Digital Soles con saldo S/ 500.00
INSERT INTO cuentas (cliente_id, numero_cuenta, tipo, moneda, saldo, tea)
VALUES (
    (SELECT id FROM clientes WHERE dni = '75280128'),
    '40012345678901',
    'Cuenta Digital Soles',
    'PEN',
    500.00,
    4.00
);

-- Empleado demo (password: 123456)
INSERT INTO empleados (codigo_empleado, nombres, apellidos, password, cargo, estado)
VALUES (
    'EMP001',
    'CARLOS',
    'GARCIA MENDOZA',
    '$2b$12$.fcfYhi/ZoRGMyEvutTtWu.9g.UzyqqG8ar4eH4CNd16dz0VwsaC.',
    'ASESOR DE SERVICIO',
    'ACTIVO'
);

-- Notificación de bienvenida
INSERT INTO notificaciones (cliente_id, tipo, titulo, descripcion)
VALUES (
    (SELECT id FROM clientes WHERE dni = '75280128'),
    'BIENVENIDA',
    '¡Bienvenido a Compartamos Banco!',
    'Tu cuenta digital ha sido creada exitosamente. Disfruta de nuestros servicios.'
);
