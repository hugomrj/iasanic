from sanic import Sanic, Request
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



# --- Endpoint: /generate/ ---
@app.post("/generate/")
async def generate_text_with_gemma(request: Request):
    try:
        data = request.json
        if not data or "prompt" not in data:
            return json({"error": "Falta el campo 'prompt'"}, status=400)

        prompt = data["prompt"]
        # CAMBIO: Agregamos await porque get_gemma_response ahora es async
        gemma_output = await get_gemma_response(prompt) 
        return json({"response": gemma_output})
    except Exception as e:
        return json({"error": f"Error al generar contenido: {str(e)}"}, status=500)






@app.post("/generate_rag")
async def generate_response(request: Request):
    try:
        data = request.json or {}
        print(f"REQ RAG: {data.get('user_query', 'N/A')[:50]}...")

        rag_response = await generate_rag_response(
            data.get("user_query", ""), 
            data.get("intencion", ""), 
            data.get("resumen", ""), 
            data.get("datos", "")
        )

        print(f"RES RAG: OK")
        return json({"response": rag_response})
    except Exception as e:
        print(f"ERR RAG: {str(e)}")
        return json({"error": f"Error interno: {str(e)}"}, status=500)






# --- Endpoint: /analyze_question/ ---
@app.post("/analyze_question/")
async def analyze_question(request: Request):
    try:
        data = request.json or {}
        pregunta = data.get("question", "N/A")
        
        # Log minimalista: Entrada
        print(f"REQ: {pregunta[:50]}...") 

        analysis_result = await analyze_question_with_ai(
            pregunta,
            intension=data.get("intension", "").strip()
        )

        # Log minimalista: Salida
        print(f"RES: {analysis_result.get('tipo', 'error')}")
        
        return json(analysis_result, ensure_ascii=False)
    except Exception as e:
        print(f"ERR: {str(e)}")
        return json({"error": str(e)}, status=500)






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


    