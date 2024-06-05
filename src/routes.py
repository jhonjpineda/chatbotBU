import re
import logging
from flask import Blueprint, render_template, request, jsonify
import openai
import os
from .pdf_processor import extract_text_from_pdf
from .config import Config

main_routes = Blueprint('main', __name__)

openai.api_key = Config.OPENAI_API_KEY

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant who answers questions strictly based on the following knowledge base."},
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Answer based only on the knowledge base provided."}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pdf_path = os.path.join(base_dir, 'data', 'knowledge_base.pdf')
knowledge_base = extract_text_from_pdf(pdf_path)

@main_routes.route('/')
def home():
    return render_template('index.html')

@main_routes.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_input = data.get('question', '')
    if not is_valid_input(user_input):
        return jsonify({'response': 'Entrada inválida. Por favor, inténtalo de nuevo.'})
    prompt = f"Knowledge base: {knowledge_base}\n\nUser: {user_input}\nAI:"
    response = generate_response(prompt)
    return jsonify({'response': response})

def is_valid_input(user_input):
    return bool(re.match("^[\w\s,.\?!áéíóúÁÉÍÓÚñÑ]*$", user_input))

@main_routes.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"An error occurred: {e}")
    return jsonify({'response': 'Ocurrió un error en el servidor. Por favor, inténtalo de nuevo más tarde.'}), 500
