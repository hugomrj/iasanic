# app/config.py
import json
from pathlib import Path
import google.generativeai as genai
import random


def load_api_keys():
    """Carga las API Keys desde google_keys.json o devuelve lista vacía si falla"""
    try:
        with open(Path(__file__).parent / "google_keys.json") as f:
            return json.load(f).get("GOOGLE_API_KEYS", [])
    except:
        return []




class Settings:
    def __init__(self):

        self.google_api_keys = load_api_keys()
        #self.gemma_model_name = "gemma-3-12b-it"
        self.gemma_model_name = "gemini-2.5-flash-lite"

        #self.gemma_temperature = 0.9
        self.gemma_temperature = 0

        self.gemma_top_p = 1.0
        self.gemma_top_k = 40
        self.gemma_max_output_tokens = 2048



    def get_random_key(self):
        """Selecciona y configura una API key aleatoria"""
        if not self.google_api_keys:
            raise ValueError("No hay claves API configuradas")
        selected_key = random.choice(self.google_api_keys)
        genai.configure(api_key=selected_key)
        # print(selected_key)
        return selected_key  # Opcional para logging



# Instancia global de configuración
settings = Settings()

