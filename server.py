from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import uvicorn

# Inicializar la aplicación FastAPI
app = FastAPI(title="Da&Da Solutions - Agente IA API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos del frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Modelo de datos para la solicitud
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"

# Modelo de datos para la respuesta
class SourceDoc(BaseModel):
    source: str
    content_snippet: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceDoc]

@app.get("/")
async def read_index():
    """Sirve la página HTML principal."""
    return FileResponse(os.path.join("frontend", "index.html"))

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Recibe la pregunta del usuario, la procesa con RAG y devuelve la respuesta."""
    try:
        from src.agent import get_agent
        
        # Obtener el agente RAG (singleton)
        agent = get_agent()
        
        # Ejecutar la cadena con la pregunta del usuario y el ID de sesión para memoria
        result = agent.invoke(
            {"input": request.message},
            config={"configurable": {"session_id": request.session_id}}
        )
        
        # Extraer la respuesta
        answer = result["answer"]
        
        # Extraer las fuentes (metadatos de los documentos recuperados)
        sources = []
        if "context" in result:
            for doc in result["context"]:
                # Obtener el nombre del archivo de la ruta completa asegurando que funcione en Linux y Windows
                source_path = doc.metadata.get("source", "Desconocido")
                filename = source_path.replace('\\', '/').split('/')[-1]
                
                # Obtener un pequeño snippet del contenido (primeros 100 caracteres)
                snippet = doc.page_content[:100].replace("\n", " ") + "..."
                
                # Evitar fuentes duplicadas exactas
                if not any(s.source == filename and s.content_snippet == snippet for s in sources):
                    sources.append(SourceDoc(source=filename, content_snippet=snippet))
        
        return ChatResponse(answer=answer, sources=sources)
        
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail="Índice vectorial no encontrado. Ejecuta ingest.py primero.")
    except Exception as e:
        print(f"Error en el endpoint de chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

from src.config import BASE_DIR

@app.get("/api/docs")
async def get_docs():
    """Devuelve la lista de documentos en la carpeta docs/"""
    docs_dir = os.path.join(BASE_DIR, "docs")
    try:
        if not os.path.exists(docs_dir):
            return {"docs": []}
        files = [f for f in os.listdir(docs_dir) if f.endswith(('.pdf', '.txt', '.csv'))]
        return {"docs": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Iniciando servidor FastAPI en el puerto 8000...")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
