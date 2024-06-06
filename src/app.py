import logging
from flask import Flask, request, jsonify
from flask_wtf.csrf import CSRFProtect
from src.routes import main_routes
from src.config import Config
from src.pdf_processor import extract_texts_from_all_pdfs
import openai

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    csrf = CSRFProtect(app)
    app.register_blueprint(main_routes)
    
    logging.basicConfig(level=logging.INFO)
    
    return app

app = create_app()

# Configurar la clave de API de OpenAI
openai.api_key = app.config['OPENAI_API_KEY']

# Cargar textos de todos los PDFs en el directorio de documentos
documents_dir = app.config['DOCUMENTS_DIR']
knowledge_base_text = extract_texts_from_all_pdfs(documents_dir)
print(f"Knowledge base loaded with text: {knowledge_base_text[:500]}...")  # Depuración

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("question")
    print(f"Received question: {user_input}")  # Depuración
    prompt = f"Knowledge base: {knowledge_base_text}\n\nUser: {user_input}\nAI:"
    response = generate_response(prompt)
    print(f"Response: {response}")  # Depuración
    return jsonify({"response": response})

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

if __name__ == "__main__":
    from waitress import serve
    serve(app, host='127.0.0.1', port=8000)
