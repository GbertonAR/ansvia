import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
from openai import AzureOpenAI

# === Cargar configuración desde .env ===
load_dotenv()
AOAI_ENDPOINT = os.getenv("AOAI_ENDPOINT")
AOAI_KEY = os.getenv("AOAI_KEY")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
API_VERSION = os.getenv("API_VERSION")

# === Inicializar cliente de Azure OpenAI ===
client = AzureOpenAI(
    api_key=AOAI_KEY,
    azure_endpoint=AOAI_ENDPOINT,
    api_version=API_VERSION
)

# === Inicializar Flask ===
app = Flask(__name__)
CORS(app)

# === Extraer texto de un PDF ===
def extract_text_from_pdf(file_stream):
    text_pages = []
    try:
        reader = PdfReader(file_stream)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_pages.append(text)
    except Exception as e:
        print("Error al leer PDF:", e)
    return text_pages

# === Dividir texto en fragmentos seguros (por caracteres) ===
def split_text(text, max_chars=9000):
    fragments = []
    while len(text) > max_chars:
        split_at = text.rfind("\n", 0, max_chars)
        if split_at == -1:
            split_at = max_chars
        fragments.append(text[:split_at].strip())
        text = text[split_at:].strip()
    if text:
        fragments.append(text)
    return fragments

# === Analizar documentos usando Azure OpenAI con división automática ===
def analyze_documents_with_openai(documents: dict, question: str):
    full_context = "\n\n".join(
        f"Archivo: {filename}\n" + "\n".join(pages)
        for filename, pages in documents.items()
    )

    fragments = split_text(full_context)
    partial_summaries = []

    for i, fragment in enumerate(fragments):
        print(f"Procesando fragmento {i+1}/{len(fragments)}")
        messages = [
            {"role": "system", "content": "Eres un asistente legal que resume documentos por partes."},
            {"role": "user", "content": f"Parte {i+1}:\n{fragment}\n\nPregunta: {question}"}
        ]
        try:
            response = client.chat.completions.create(
                model=DEPLOYMENT_NAME,
                messages=messages,
                max_tokens=800,
                temperature=0.7
            )
            content = response.choices[0].message.content
            partial_summaries.append(content)
        except Exception as e:
            print(f"Error en fragmento {i+1}:", e)
            partial_summaries.append(f"[Error en fragmento {i+1}]")

    # Hacer resumen final
    final_context = "\n\n".join(partial_summaries)
    messages = [
        {"role": "system", "content": "Eres un asistente legal que resume múltiples partes."},
        {"role": "user", "content": f"Basado en estos fragmentos parciales, responde de forma completa a la pregunta:\n{question}\n\nFragmentos:\n{final_context}"}
    ]

    try:
        final_response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=messages,
            max_tokens=800,
            temperature=0.7
        )
        return final_response.choices[0].message.content
    except Exception as e:
        print("Error en resumen final:", e)
        return f"Error: {str(e)}"

# === Ruta Flask para subir y analizar PDFs ===
@app.route("/ask", methods=["POST"])
def ask():
    try:
        question = request.form.get("pregunta")
        files = request.files.getlist("archivos")

        if not question or not files:
            return jsonify({"error": "Debe incluir pregunta y al menos un archivo PDF"}), 400

        documents = {}
        for file in files:
            text_pages = extract_text_from_pdf(file.stream)
            if text_pages:
                documents[file.filename] = text_pages

        print(f"Analizando {len(files)} archivos con la pregunta: {question}")
        answer = analyze_documents_with_openai(documents, question)
        print(">>> Respuesta:", answer)

        if not answer:
            return jsonify({"error": "No se pudo generar una respuesta"}), 500

        return jsonify({"answer": answer})
    except Exception as e:
        print("Error general:", e)
        return jsonify({"error": str(e)}), 500

# === Iniciar servidor ===
if __name__ == "__main__":
    app.run(debug=False)
