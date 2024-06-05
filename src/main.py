import os
from pdf_processor import extract_text_from_pdf
import openai

openai.api_key = 'sk-proj-KLGKEZokVfMnZsQupmVDT3BlbkFJWLs3EgPBM3qsqEOVgixX'

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
    pdf_path = os.path.join(base_dir, 'data', 'knowledge_base.pdf')
    
    try:
        knowledge_base = extract_text_from_pdf(pdf_path)
        print("Knowledge base loaded. You can start asking questions.")
        
        while True:
            user_input = input("You: ")
            prompt = f"Knowledge base: {knowledge_base}\n\nUser: {user_input}\nAI:"
            response = generate_response(prompt)
            print(f"AI: {response}")
    
    except FileNotFoundError:
        print(f"Error: The file at path {pdf_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
