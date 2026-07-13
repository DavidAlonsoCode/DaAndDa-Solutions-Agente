import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env (y .env.cohere)
load_dotenv()

# Directorios
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
FAISS_INDEX_DIR = os.path.join(BASE_DIR, "faiss_index")

# Configuraciones de RAG
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Claves de API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("⚠️ No se encontró GOOGLE_API_KEY en las variables de entorno.")
