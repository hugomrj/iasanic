

def normalizar_nombre (nombre: str) -> str:
    grupos = {
        "asistente_nombre": [
            "quien_soy",
            "identidad"
        ],
        "saludo": [
            "saludo",
            "hola",
            "buen_dia"
        ],
        "obtener_facturacion": [
            "obtener_facturacion_anual",
            "facturacion_anual",
            "obtener_facturacion_por_anio",
            "obtener_facturacion_por_año",
        ],
        "clientes_mas_compras": [
            "obtener_clientes_mas_compras",
            "obtener_clientes_mas_compradores",
            "obtener_clientes_top_compras",
            "obtener_clientes_con_mas_compras",
            "obtener_clientes_mas_compraron",
            "obtener_clientes_top_compradores",
            "listar_compradores_top",
            "obtener_compradores_top"
        ],







        # Agregás más grupos según necesites
    }

    for funcion_canonica, sinonimos in grupos.items():
        if nombre in sinonimos:
            return funcion_canonica

    return nombre  # Si no hay coincidencia, se devuelve tal cual

