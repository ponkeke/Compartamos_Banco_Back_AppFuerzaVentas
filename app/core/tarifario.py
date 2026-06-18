# Tarifario de productos de crédito - Compartamos Banco
# Tasas referenciales (TEA) por producto
# Estas tasas se asignan en la evaluación y desembolso
# NO hardcodear en Flutter; consumir desde el Core

TARIFARIO = {
    "CrediMujer": {
        "nombre": "CrediMujer",
        "tea": 32.00,
        "tea_max": 38.00,
        "seguro": 0.50,
        "plazo_min": 6,
        "plazo_max": 48,
        "monto_min": 500.00,
        "monto_max": 15000.00,
    },
    "CrediChamba": {
        "nombre": "CrediChamba",
        "tea": 36.00,
        "tea_max": 42.00,
        "seguro": 0.50,
        "plazo_min": 3,
        "plazo_max": 36,
        "monto_min": 300.00,
        "monto_max": 8000.00,
    },
    "CrediNegocio": {
        "nombre": "CrediNegocio",
        "tea": 28.00,
        "tea_max": 34.00,
        "seguro": 0.50,
        "plazo_min": 6,
        "plazo_max": 60,
        "monto_min": 1000.00,
        "monto_max": 50000.00,
    },
    "CrediViaje": {
        "nombre": "CrediViaje",
        "tea": 38.00,
        "tea_max": 44.00,
        "seguro": 0.50,
        "plazo_min": 3,
        "plazo_max": 24,
        "monto_min": 500.00,
        "monto_max": 10000.00,
    },
}


def obtener_tasa_producto(tipo_credito: str) -> float | None:
    producto = TARIFARIO.get(tipo_credito)
    if producto:
        return producto["tea"]
    return None


def obtener_seguro_producto(tipo_credito: str) -> float:
    producto = TARIFARIO.get(tipo_credito)
    if producto:
        return producto["seguro"]
    return 0.50


def calcular_cuota_estimada(monto: float, tea: float, numero_cuotas: int) -> float:
    # Conversión TEA a TEM (tasa efectiva mensual)
    tem = ((1 + tea / 100) ** (1 / 12)) - 1
    if tem == 0:
        return monto / numero_cuotas
    factor = (tem * (1 + tem) ** numero_cuotas) / ((1 + tem) ** numero_cuotas - 1)
    return round(monto * factor, 2)
