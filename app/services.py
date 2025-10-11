# app/services.py
import datetime
import json
import google.generativeai as genai
from app.config import settings
from app.normalizador import normalizar_nombre
from dateutil.relativedelta import relativedelta
from datetime import date



def get_gemma_response(prompt: str, max_retries: int = 2) -> str:
    """
    Envía un prompt al modelo Gemma y retorna su respuesta de texto.
    """
    last_error = None

    for attempt in range(max_retries):
        try:
            key = settings.get_random_key()
            model = genai.GenerativeModel(settings.gemma_model_name)

            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.0,
                    top_p=1.0,
                    top_k=1,
                    max_output_tokens=512
                )
            )

            print(response.text)

            return response.text or "No se pudo generar respuesta a la solicitud"

        except Exception as e:
            last_error = e
            print(f"Intento {attempt+1} fallido (key: {key[-6:]}) - Error: {str(e)[:200]}")
            continue

    print(f"Fallo definitivo. Último error: {str(last_error)[:300]}")
    raise RuntimeError("Error al procesar la solicitud. Intente nuevamente.")







def generate_rag_response(user_query: str, context: str, datos: str = "", max_retries: int = 2) -> str:
    """
    Genera una respuesta RAG con intento automático de reintentos.

    Args:
        user_query: Pregunta del usuario (obligatorio)
        context: Contexto RAG (obligatorio o vacío)
        datos: Dato extraído directamente del RAG o de la base (opcional)
        max_retries: Número de intentos en caso de error
    """
    last_error = None

    # Construye el prompt con la sección de datos si está disponible
    prompt = build_rag_prompt(user_query, context, datos)

    for attempt in range(max_retries):
        try:
            key = settings.get_random_key()
            model = genai.GenerativeModel(settings.gemma_model_name)

            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.0,
                    top_p=1.0,
                    top_k=1,
                    max_output_tokens=512
                )
            )

            print(response.text)

            return response.text or "No se pudo generar respuesta a la solicitud"

        except Exception as e:
            last_error = e
            print(f"Intento {attempt+1} fallido (key: {key[-6:]}) - Error: {str(e)[:200]}")
            continue

    print(f"Fallo definitivo. Último error: {str(last_error)[:300]}")
    raise RuntimeError("Error al procesar la solicitud. Intente nuevamente.")













def build_rag_prompt(user_query: str, context: str, datos: str = "") -> str:
    """
    Genera un prompt RAG con formato estructurado y claro.
    """
    PROMPT_TEMPLATE = """
# sistema
Eres un asistente especializado, que responde con la información dada, sin inventar.
Indica si la funcion no esta implementada
Prioriza siempre la pregunta del usuario sobre los datos encontrados.

# personalidad
Amable, claro y profesional.

# configuracion
- idioma: español
- moneda: guaraní Gs.

# REGLAS
- No termines con otra pregunta.
- No expliques más de lo necesario.
- Mantén los números exactos como en los datos.
- Muestra valores numericos de montos en negritas
- Si dato 'nivel de claridad del mensaje' es 'media', solicita mas informacion sin dar ejemplos.
- En caso que la funcion no este implementada, informa nombre de la funcion tal como es

# contexto
{context}

# datos
{datos_section}

# pregunta
{user_query}
    """

    datos_section = datos if datos else "No se encontró información específica en los datos disponibles."

    prompt = PROMPT_TEMPLATE.format(
        user_query=user_query.strip(),
        context=context.strip(),
        datos_section=datos_section.strip()
    )


    print(prompt)

    return prompt.strip()




def generate_structured_response(prompt: str, max_retries: int = 2) -> str:
    """
    Genera respuesta determinista para RAG con:
    - Rotación automática de claves
    - 2 reintentos automáticos
    - Logging seguro
    """
    last_error = None

    for attempt in range(max_retries):
        try:
            key = settings.get_random_key()  # Configura nueva key automáticamente
            model = genai.GenerativeModel(settings.gemma_model_name)

            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.0,
                    top_p=1.0,
                    top_k=1,
                    max_output_tokens=512
                )
            )


            print(response.text)

            return response.text or "No se pudo generar respuesta estructurada"

        except Exception as e:
            last_error = e
            print(f"Intento {attempt+1} fallido (key: {key[-6:]}) - Error: {str(e)[:200]}")
            continue

    print(f"Fallo definitivo. Último error: {str(last_error)[:300]}")
    raise RuntimeError("Error al procesar la solicitud. Intente nuevamente.")











def analyze_question_with_ai(user_question: str) -> dict:
    prompt = f"""
    configuracion:
    idioma: español
    formato: json
    reglas:
    - Inferir ambigüedades
    - No explicaciones
    - Retornar vacío si no se entiende
    - campo funcion:
        - Genera nombre más comun, corto, claro y utilizado,
        - Prioriza el uso de sustantivos y complementos relevantes.
        - Omite palabras redundantes o poco informativas.

    - claridad: "Evaluar lógica y coherencia de solicitud"
    - campo parametros:
        - Inferir valores completos y correctos para la función especificada
        - Valor en snake_case
    estructura_salida:
    funcion: "snake_case"
    palabras_clave: "lista"
    entidades: "lista objetos"
    intencion: "deducir proposito de solicitud muy breve"
    resumen: "frase breve"
    confianza: "1-9"
    claridad: "alta | media | baja"
    original: "corregido"
    parametros: {{"clave": "valoe"}}


    solicitud: >
        {user_question}
    """.strip()

    response = generate_structured_response(prompt)

    # Limpieza del JSON
    json_str = (
        response.strip()
        .removeprefix('```json')
        .removesuffix('```')
        .strip()
    )


    try:
        result = json.loads(json_str)
    except json.JSONDecodeError:
        result = {
            "error": "JSON inválido",
            "respuesta_ia": response,
            "original": user_question
        }

    # Si JSON válido, normalizar y devolver dict
    return normalize_before_retrieval(result)
    #return result






def normalize_before_retrieval(data: dict) -> dict:


    if "error" in data:
        return {
            "funcion": "error_json_invalido",
            "parametros": {},
            "resumen": data.get("error", "Error desconocido"),
            "palabras_clave": [],
            "confianza": 0,
            "claridad": "baja",
            "original": data.get("original", ""),
            "estado": "rechazado"
        }

    data.setdefault("funcion", "")
    if not data["funcion"]:
        data["funcion"] = "invalida"

    data.setdefault("resumen", "")
    data.setdefault("palabras_clave", [])
    data.setdefault("parametros", {})
    data.setdefault("confianza", 1)
    data.setdefault("original", "")



    # Limpiar "date:" si está en el parámetro
    ''''
    fecha = data["parametros"].get("fecha", "")
    if fecha.startswith("date:"):
        data["parametros"]["fecha"] = fecha[5:]
    '''


    if data.get("claridad") == "alta":

        data["estado"] = "aprobado"


        # Atajos para evitar repetir
        palabra_clave= data.get("palabras_clave", [])  # tokens clave detectados
        parametro = data["parametros"]  # donde se guardarán todos los parámetros

        hoy = datetime.date.today()


        # en el parámetro 'fecha' usando un diccionario de conversión precalculado
        fecha = {
            "hoy": hoy.strftime("%Y-%m-%d"),
            "ayer": (hoy - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),  # Resta 1 día
            "mañana": (hoy + datetime.timedelta(days=1)).strftime("%Y-%m-%d")  # Suma 1 día
        }
        for clave, valor in parametro.items():
            # Solo normaliza si el valor es EXACTAMENTE un string (no lista u otro tipo)
            if isinstance(valor, str) and valor in fecha:
                parametro[clave] = fecha[valor]





        param_keys = list(parametro.keys())
        for key in param_keys:
            if key.lower() == "periodo":
                valor = str(parametro.pop(key)).strip().lower()

                match valor:
                    case "mes":
                        parametro["mes_actual"] = hoy.strftime("%Y-%m")
                    case "mes_anterior":
                        parametro["mes_anterior"] = (hoy - relativedelta(months=1)).strftime("%Y-%m")
                    case "mes_siguiente":
                        parametro["mes_siguiente"] = (hoy + relativedelta(months=1)).strftime("%Y-%m")
                    case "año_actual":
                        parametro["año_actual"] = hoy.strftime("%Y")  # Solo el año (2024)
                    case "año_anterior":
                        parametro["año_anterior"] = str(hoy.year - 1)  # 2023
                    case "año_siguiente":
                        parametro["año_siguiente"] = str(hoy.year + 1)  # 2025
                    case _:
                        parametro[key] = valor  # Conserva el original





    elif data.get("claridad") == "media":
        data["funcion"] = "pendiente_aclaracion"
        data["estado"] = "pendiente"


    else:
        data["funcion"] = "desconocida"
        data["estado"] = "rechazado"





    # ⬇️ Normalizar el nombre de la función aquí
    data["funcion"] = normalizar_nombre(data["funcion"])


    # Ahora construimos el diccionario de salida con el orden deseado
    ordered_data = {
        "funcion": data["funcion"],
        "parametros": data["parametros"],
        "palabras_clave": data["palabras_clave"],
        "entidades": data.get("entidades", []),
        "intencion": data.get("intencion", ""),
        "resumen": data["resumen"],
        "confianza": data["confianza"],
        "claridad": data.get("claridad", ""),
        "original": data["original"],
        "estado": data.get("estado", "")
    }

    return ordered_data



