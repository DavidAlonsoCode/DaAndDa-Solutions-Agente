from src.document_loader import load_and_split_documents
from src.vector_store import create_and_save_index

def run_ingestion():
    print("🚀 Iniciando el proceso de ingestión RAG...")
    
    # 1. Cargar y dividir los PDFs
    chunks = load_and_split_documents()
    
    if not chunks:
        print("❌ Proceso abortado: No hay documentos para indexar.")
        return
        
    # 2. Generar embeddings y guardar en FAISS
    create_and_save_index(chunks)
    
    print("✨ Ingestión completada exitosamente.")

if __name__ == "__main__":
    run_ingestion()
