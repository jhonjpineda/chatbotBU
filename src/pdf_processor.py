import os
import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
    return text

def extract_texts_from_all_pdfs(directory):
    all_texts = ""
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            print(f"Processing file: {file_path}")  # Depuración
            text = extract_text_from_pdf(file_path)
            print(f"Extracted text from {file_path}: {text[:100]}...")  # Depuración
            all_texts += text + "\n"  # Asegurarse de separar textos con un salto de línea
    return all_texts
