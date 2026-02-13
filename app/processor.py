# app/processor.py
import datetime
from .normalizador import normalizar_nombre_funcion
from dateutil.relativedelta import relativedelta

def process_intent(data: dict) -> dict:
    if "error" in data:
        return data

    # 1. CAPTURAMOS AMBOS NOMBRES
    # Guardamos lo que envió la IA originalmente
    funcion_ia = data.get("funcion") or ""
    
    # Creamos la versión normalizada
    if isinstance(funcion_ia, str) and funcion_ia.strip():
        funcion_procesada = normalizar_nombre_funcion(funcion_ia)
    else:
        funcion_procesada = ""

    # 2. PROCESAR PARÁMETROS
    parametros = data.get("parametros") if isinstance(data.get("parametros"), dict) else {}
    if parametros:
        hoy = datetime.date.today()
        mapa_fechas = {
            "hoy": hoy.strftime("%Y-%m-%d"),
            "ayer": (hoy - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            "mañana": (hoy + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        }

        for key in list(parametros.keys()):
            valor = parametros[key]
            if isinstance(valor, str):
                v_lower = valor.lower().strip()
                if v_lower in mapa_fechas:
                    parametros[key] = mapa_fechas[v_lower]
                
                if key.lower() == "periodo":
                    parametros.pop(key)
                    match v_lower:
                        case "mes": parametros["mes_actual"] = hoy.strftime("%Y-%m")
                        case "mes_anterior": parametros["mes_anterior"] = (hoy - relativedelta(months=1)).strftime("%Y-%m")
                        case "mes_siguiente": parametros["mes_siguiente"] = (hoy + relativedelta(months=1)).strftime("%Y-%m")
                        case "año_actual": parametros["año_actual"] = str(hoy.year)
                        case "año_anterior": parametros["año_anterior"] = str(hoy.year - 1)
                        case "año_siguiente": parametros["año_siguiente"] = str(hoy.year + 1)
                        case _: parametros[key] = v_lower

    # 3. RETORNO (Aquí es donde aparecen las dos llaves)
    return {        
        "tipo": data.get("tipo", "informacion"),
        "funcion": funcion_procesada,       # La normalizada
        "funcion_ia": funcion_ia,           # La original de la IA
        "parametros": parametros,
        "palabras_clave": data.get("palabras_clave", []),
        "entidades": data.get("entidades", []),
        "intencion": data.get("intencion", ""),
        "resumen": data.get("resumen", ""),
        "confianza": data.get("confianza", 0),
        "claridad": data.get("claridad", "baja"),
        "original": data.get("original", "")
    }