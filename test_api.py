import requests
import json
import time

URL = "http://localhost:8000/analyze_question/"


preguntas = [

    # ========== VENTAS POR MES (obtener_ventas) ==========
    "¿Cuánto facturamos durante marzo?",
    "Dame las ventas del mes de marzo",
    "Necesito los ingresos de marzo",
    "¿A cuánto ascendió la facturación en el mes de marzo?",
    "Mostrame lo que se vendió en marzo",
    
    

]






for i, pregunta in enumerate(preguntas, start=1):

    
    print(f"\n🟦 Pregunta {i}: {pregunta}")
    try:
        res = requests.post(URL, json={"question": pregunta}, timeout=10)
        res.raise_for_status()
        data = res.json()

        print("🟩 Respuesta:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

    except requests.RequestException as e:
        print(f"❌ Error con la pregunta {i}: {e}")

    time.sleep(3)   

print("\n✅ Finalizado. Todas las respuestas fueron mostradas.")
