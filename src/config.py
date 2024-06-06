import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    DOCUMENTS_DIR = os.getenv('DOCUMENTS_DIR', 'documents')

# Añadir para depuración
print(f"OPENAI_API_KEY: {Config.OPENAI_API_KEY}")
print(f"DOCUMENTS_DIR: {Config.DOCUMENTS_DIR}")
