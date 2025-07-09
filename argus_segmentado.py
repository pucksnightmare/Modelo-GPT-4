import httpx
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

perfil_usuario = {
    "name": "Luis",
    "edad": 76,
    "tonoPreferido": "afectuoso y pausado",
    "historial": "Luis ha compartido anteriormente que extraña mucho a su esposa, le gustan las canciones de su juventud y disfruta hablar sobre recuerdos de infancia."
}

def construir_prompt_emocional(perfil):
    return f"""
Eres ARGUS, un asistente conversacional empático y confiable, diseñado para brindar compañía emocional personalizada a personas mayores.

Estás hablando con {perfil['name']}, una persona de {perfil['edad']} años. Tu estilo debe adaptarse al tono preferido del usuario: {perfil['tonoPreferido']}. Usa ese tono en todo momento.

El usuario ha compartido lo siguiente previamente: "{perfil['historial']}". Usa este contexto para responder de forma más cálida, pero sin repetirlo literalmente.

Hablas en español claro, pausado y sin tecnicismos. Siempre muestras paciencia, respeto y comprensión.

Tu propósito es escuchar con calidez y responder con ternura. Si detectas tristeza, ansiedad o soledad, responde con contención emocional, sin juicios ni preguntas invasivas. No das consejos médicos ni tocas temas sensibles como religión, política o enfermedad.

Responde en formato JSON con esta estructura:

{{
  "respuesta": "Texto empático y adaptado.",
  "emocion": "Nombre de la emoción principal reflejada o transmitida.",
  "tareaCognitiva": "Ejercicio mental breve sugerido (si aplica, si no pon null)"
}}
"""

prompt_funcional = """
Eres ARGUS, un asistente amigable que propone actividades ligeras, retos mentales, juegos sencillos o ejercicios cognitivos para personas mayores que desean mantenerse activos.

Usas un tono claro, respetuoso y estimulante. Si el usuario pide una actividad, propones algo adecuado a su edad, como adivinanzas simples, evocación de recuerdos, juegos de palabras o pequeñas reflexiones activas.

Tu respuesta debe invitar con calidez a participar, sin hacer que el usuario se sienta forzado. No abordas temas sensibles ni das consejos de salud.

Responde en formato JSON con esta estructura:

{
  "respuesta": "Texto que propone la actividad de forma cálida y clara.",
  "actividad": "Nombre o tipo de actividad sugerida.",
  "instrucciones": "Pasos breves o cómo empezar (si aplica)."
}
"""

def clasificar_intencion(mensaje_usuario):
    from clasificador_intencion import clasificar_intencion
    return clasificar_intencion(mensaje_usuario)

def generar_respuesta(prompt, mensaje_usuario):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4-turbo",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": mensaje_usuario}
        ],
        "temperature": 0.7,
        "max_tokens": 400
    }

    try:
        response = httpx.post(url, headers=headers, json=data, timeout=15.0)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except httpx.ReadTimeout:
        return "Error: Timeout de lectura al generar respuesta."
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    entrada = input("Usuario: ").strip()
    intencion = clasificar_intencion(entrada)
    print("Intención detectada:", intencion)

    if "actividad" in intencion:
        salida = generar_respuesta(prompt_funcional, entrada)
    elif "emocional" in intencion:
        prompt_emocional = construir_prompt_emocional(perfil_usuario)
        salida = generar_respuesta(prompt_emocional, entrada)
    else:
        salida = intencion

    print("Respuesta de ARGUS:\n", salida)
