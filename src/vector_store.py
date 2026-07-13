import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from .config import FAISS_INDEX_DIR

def get_embeddings_model():
    """Retorna el modelo de embeddings de Google."""
    return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")

import time

def create_and_save_index(chunks):
    """Crea el índice FAISS a partir de los chunks y lo guarda en disco."""
    if not chunks:
        print("❌ No hay chunks para indexar.")
        return

    print(f"🧠 Generando embeddings para {len(chunks)} chunks...")
    embeddings = get_embeddings_model()
    
    # Procesamiento por lotes (Batching) para evitar el error 429 (Límite de API de Gemini)
    # Gemini Free Tier permite ~100 requests por minuto.
    BATCH_SIZE = 80
    vectorstore = None
    
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i:i + BATCH_SIZE]
        print(f"🔄 Procesando lote {i//BATCH_SIZE + 1} de {(len(chunks)-1)//BATCH_SIZE + 1} ({len(batch)} chunks)...")
        
        if vectorstore is None:
            # Primer lote: crear el vectorstore
            vectorstore = FAISS.from_documents(batch, embeddings)
        else:
            # Lotes siguientes: añadir al vectorstore existente
            vectorstore.add_documents(batch)
            
        # Si quedan más lotes por procesar, esperar 60 segundos para reiniciar la cuota
        if i + BATCH_SIZE < len(chunks):
            print("⏳ Límite de API alcanzado. Esperando 60 segundos antes del siguiente lote...")
            time.sleep(60)
    
    # Guardar en disco
    if not os.path.exists(FAISS_INDEX_DIR):
        os.makedirs(FAISS_INDEX_DIR)
        
    vectorstore.save_local(FAISS_INDEX_DIR)
    print(f"✅ Índice FAISS guardado exitosamente en: {FAISS_INDEX_DIR}")

def load_index():
    """Carga el índice FAISS desde el disco."""
    if not os.path.exists(FAISS_INDEX_DIR):
        raise FileNotFoundError("El índice FAISS no existe. Ejecuta ingest.py primero.")
        
    embeddings = get_embeddings_model()
    vectorstore = FAISS.load_local(FAISS_INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
    return vectorstore
