import difflib
import unicodedata
import re


def normalizar_nombre_funcion(nombre: str) -> str:
    
    """Función principal: aplica todas las etapas de normalización."""
    nombre = limpiar_texto(nombre)
    nombre = normalizar_raiz(nombre)
    nombre = normalizar_prefijos(nombre)
    nombre = reemplazar_sinonimos(nombre)
    nombre = normalizar_sufijos_funcion(nombre)
    nombre = evitar_duplicados(nombre)
    nombre = reemplazar_expresiones(nombre)
    nombre = eliminar_palabras(nombre)

    return nombre





def limpiar_texto(nombre: str) -> str:
    """Limpia espacios, mayúsculas, tildes y normaliza separadores."""
    nombre = nombre.strip().lower().replace(" ", "_")
    # 🔹 Eliminar tildes y acentos
    nombre = ''.join(
        c for c in unicodedata.normalize('NFD', nombre)
        if unicodedata.category(c) != 'Mn'
    )
    while "__" in nombre:
        nombre = nombre.replace("__", "_")
    return nombre



def normalizar_raiz(nombre: str) -> str:
    """Ajusta raíces verbales para mantener consistencia semántica."""
    grupos = {
        "facturacion": ["facturado", "facturadas", "facturados"],
        "ventas": ["vendido", "vendidos", "vendidas", "vendida"],
        "cobros": ["cobrado", "cobrados", "cobradas"],
        "productos": ["producto"],
    }

    for reemplazo, palabras in grupos.items():
        for palabra in palabras:
            # escapamos la palabra para evitar metacaracteres
            p = re.escape(palabra)
            # capturamos el separador anterior y posterior (inicio|_ , _|fin)
            pattern = rf'(^|_)({p})(_|$)'
            # reemplazamos manteniendo los separadores
            nombre = re.sub(pattern, lambda m: f"{m.group(1)}{reemplazo}{m.group(3)}", nombre)
    return nombre





def normalizar_prefijos(nombre: str) -> str:
    """Uniformiza prefijos comunes."""
    if nombre.startswith("consultar_"):
        nombre = nombre.replace("consultar_", "obtener_", 1)
    if nombre.startswith("contar_"):
        nombre = nombre.replace("contar_", "obtener_", 1)
    if nombre.startswith("ver_"):
        nombre = nombre.replace("ver_", "obtener_", 1)
    if nombre.startswith("mostrar_"):
        nombre = nombre.replace("mostrar_", "obtener_", 1)


    return nombre





def reemplazar_sinonimos(nombre: str) -> str:
    """Reemplaza palabras por sinónimos estandarizados."""
    grupos = {
      "ventas": ["facturacion", "ingresos"],
      "compras": ["compra"],
      "productos": ["articulos", "articulo", "item", "items"],
      "vendedor": ["comercial"],
      "sucursal": ["local", "tienda"],
      "cantidad": ["volumen"],
      "mejores": ["top"],
    }

    partes = nombre.split("_")  # separamos por guiones bajos

    for i, palabra in enumerate(partes):
        for reemplazo, sinonimos in grupos.items():
            if palabra in sinonimos:
                partes[i] = reemplazo

    return "_".join(partes)



def evitar_duplicados(nombre: str) -> str:
    """Elimina palabras consecutivas duplicadas y guiones bajos extra."""
    partes = nombre.split("_")
    resultado = []

    for palabra in partes:
        if not resultado or resultado[-1] != palabra:
            resultado.append(palabra)

    return "_".join(resultado)



def reemplazar_expresiones(nombre: str) -> str:
    """Reemplaza expresiones o combinaciones de palabras."""
    expresiones = {
      "no_cobradas": ["pendiente_de_cobro", "pendientes_de_cobro", "por_cobrar"],
      "por_compras": ["por_cantidad_compras"],
      "mayor_ompras": ["mayor_cantidad_compras"],

    }

    for reemplazo, frases in expresiones.items():
        for frase in frases:
            nombre = nombre.replace(frase, reemplazo)
    return nombre







def normalizar_sufijos_funcion(nombre: str) -> str:
    """Normaliza sufijos temporales y cuantificadores en el nombre de la función."""
    grupos = {
        "mensuales": ["_mes_actual", "_del_mes", "_mes", "_por_mensuales"],
        "trimestral": ["ultimo_trimestre", "trimestre_anterior"],
        "anual": ["año_actual"],
        "total": ["_totales"],
        "promedio": ["_promedios"],
        "acumulado": ["_acumulados"],
        "parcial": ["_parciales"],
    }

    for nuevo, variantes in grupos.items():
        for viejo in variantes:
            if nombre.endswith(viejo):
                nombre = nombre[: -len(viejo)] + "_" + nuevo
                return nombre

    return nombre


def eliminar_palabras(nombre: str) -> str:
    nombre = nombre.replace("_cartera", "")
    return nombre
