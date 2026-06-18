# Compartamos Banco - Core Mobile API

Backend Core Mobile construido con **FastAPI** para la aplicación Flutter de Compartamos Banco.

## Arquitectura

```
Flutter App Clientes
    ↓ HTTP/JSON
FastAPI Core Mobile
    ↓ SQLAlchemy
PostgreSQL
```

## Requisitos

- Python 3.10+
- PostgreSQL 15+

## Instalación

```bash
# 1. Clonar repositorio
git clone <repo-url>
cd compartamos-banco-core

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de base de datos

# 5. Crear base de datos
psql -U postgres -c "CREATE DATABASE compartamos_banco_db;"
psql -U postgres -d compartamos_banco_db -f sql/schema.sql
psql -U postgres -d compartamos_banco_db -f sql/seed.sql

# 6. Ejecutar servidor
python -m uvicorn main:app --reload --port 8003
```

## Documentación Swagger

http://127.0.0.1:8003/docs

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /auth/register | Registrar nuevo cliente |
| POST | /auth/login | Iniciar sesión |
| GET | /cliente/home | Dashboard del cliente |
| GET | /contactos | Listar contactos |
| POST | /contactos | Crear contacto |
| DELETE | /contactos/{id} | Eliminar contacto |
| POST | /operaciones/yapeo | Realizar yapeo |
| POST | /operaciones/deposito | Realizar depósito |
| GET | /operaciones/movimientos | Ver movimientos |
| POST | /creditos/solicitar | Solicitar crédito |
| GET | /creditos | Listar créditos/solicitudes |
| GET | /notificaciones | Listar notificaciones |
| PUT | /notificaciones/{id}/leer | Marcar notificación leída |

## Cliente Demo

- **DNI:** 75280128
- **Password:** 123456
- **Saldo:** S/ 500.00
