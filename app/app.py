from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json, text, file
from app.services import analyze_question_with_ai, generate_rag_response, get_gemma_response
import time



app = Sanic("IA_Server")

@app.middleware("response")
async def cors_headers(request, resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return resp

@app.route("/")
async def hello(request: Request):
    return text("Hello from Sanic!")

@app.post("/generate/")
async def generate_text_with_gemma(request: Request):
    try:
        data = request.json
        if not data or "prompt" not in data:
            return json({"error": "Falta el campo 'prompt'"}, status=400)

        prompt = data["prompt"]
        gemma_output = get_gemma_response(prompt)
        return json({"response": gemma_output})
    except Exception as e:
        return json({"error": f"Error al generar contenido con Gemma: {str(e)}"}, status=500)





@app.post("/generate_rag")
async def generate_response(request: Request):
    try:
        data = request.json or {}

        user_query = data.get("user_query", "")
        datos = data.get("datos", "")
        resumen = data.get("resumen", "")
        intencion = data.get("intencion", "")

        rag_response = await generate_rag_response(
            user_query, intencion, resumen, datos
        )

        return json({"response": rag_response})

    except Exception as e:
        print("=== ERROR EN EL ENDPOINT:", str(e), "===")
        return json({"error": f"Error interno: {str(e)}"}, status=500)




from sanic import Sanic, Request
from sanic.response import json

@app.post("/analyze_question/")
async def analyze_question(request: Request):
    try:
        # En Sanic, request.json ya es el diccionario (no necesita await)
        data = request.json

        # Si no hay datos JSON
        if data is None:
            return json({"error": "Se esperaba JSON en el cuerpo"}, status=400)

        # campo obligatorio
        if "question" not in data:
            return json({"error": "El campo 'question' es requerido"}, status=400)

        user_question = data["question"].strip()
        if not user_question:
            return json({"error": "La pregunta no puede estar vacía"}, status=400)

        # campo opcional
        user_intension = data.get("intension")
        if user_intension:
            user_intension = user_intension.strip()

        print(f"Llamando a analyze_question_with_ai con: {user_question}, {user_intension}")
        
        # procesar
        analysis_result = analyze_question_with_ai(
            user_question,
            intension=user_intension
        )

        return json(analysis_result, ensure_ascii=False)

    except Exception as e:
        print(f"Error completo: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return json({"error": f"Error interno al procesar la pregunta: {str(e)}"}, status=500)









@app.route("/health")
async def health_check(request: Request):
    return json({"status": "ok"})

@app.route("/ping")
async def ping(request: Request):
    start = time.time()
    end = time.time()
    return json({
        "message": "pong",
        "response_time_ms": round((end - start) * 1000, 2)
    })



@app.route("/tester")
async def serve_tester(request):
    return await file("static/test_api.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, workers=2, access_log=False,  dev=True)


