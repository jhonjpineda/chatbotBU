import os
from dotenv import load_dotenv
from src.pdf_processor import extract_texts_from_all_pdfs
import openai

# Cargar variables de entorno desde el archivo .env
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

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
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    documents_dir = os.path.join(base_dir, 'documents')
    
    try:
        if not os.path.exists(documents_dir):
            raise FileNotFoundError
        knowledge_base = extract_texts_from_all_pdfs(documents_dir)
        print("Knowledge base loaded. You can start asking questions.")
        
        while True:
            user_input = input("You: ")
            prompt = f"Knowledge base: {knowledge_base}\n\nUser: {user_input}\nAI:"
            response = generate_response(prompt)
            print(f"AI: {response}")
    
    except FileNotFoundError:
        print(f"Error: The directory at path {documents_dir} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
