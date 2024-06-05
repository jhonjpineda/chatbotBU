import logging
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from src.routes import main_routes  # Importación correcta
from src.config import Config  # Importar configuración

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Cargar configuración desde config.py
    csrf = CSRFProtect(app)
    app.register_blueprint(main_routes)
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    return app

if __name__ == "__main__":
    app = create_app()
    
    from waitress import serve
    serve(app, host='127.0.0.1', port=8000)
