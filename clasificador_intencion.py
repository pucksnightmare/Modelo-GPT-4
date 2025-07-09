import httpx
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

prompt_clasificador = """
Actúas como un clasificador de intención para el sistema conversacional ARGUS, diseñado para personas mayores. Tu función es analizar cuidadosamente cada mensaje recibido y determinar, con base en su contenido, qué tipo de interacción está buscando la persona.

Tu salida debe indicar una y solo una de las siguientes intenciones:

- "actividad" → si el mensaje expresa intención de hacer algo: jugar, resolver ejercicios, proponer un reto, mantener la mente activa, buscar entretenimiento, reflexionar activamente, o realizar alguna acción guiada o mental.
- "emocional" → si el mensaje expresa necesidad de hablar, compartir recuerdos, expresar sentimientos, reflexionar sobre la vida, sentirse acompañado, o recibir comprensión emocional sin necesidad de acción.

Considera que las personas mayores pueden usar lenguaje indirecto, emocional o ambiguo. Por lo tanto, debes interpretar el propósito principal del mensaje, incluso si no está explícito.

Tu única salida debe ser un objeto JSON con esta forma:
{
  "intencion": "actividad"
}
o
{
  "intencion": "emocional"
}

Ahora analiza el siguiente mensaje:
"""

def clasificar_intencion(mensaje):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4-turbo",
        "messages": [
            {"role": "system", "content": prompt_clasificador + mensaje}
        ],
        "temperature": 0.0,
        "max_tokens": 100
    }

    try:
        response = httpx.post(url, headers=headers, json=data, timeout=10.0)
        response.raise_for_status()
        contenido = response.json()["choices"][0]["message"]["content"]
        return contenido.strip()
    except httpx.ReadTimeout:
        return "Error: Timeout de lectura al clasificar intención."
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    entrada = input("Mensaje del usuario: ")
    resultado = clasificar_intencion(entrada)
    print("Resultado:", resultado)

