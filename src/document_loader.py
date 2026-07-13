import os
from langchain_community.document_loaders import PyPDFLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .config import DOCS_DIR, CHUNK_SIZE, CHUNK_OVERLAP

def load_and_split_documents():
    """
    Lee todos los PDFs y CSVs del directorio de documentos y los divide en chunks.
    Retorna una lista de documentos de LangChain.
    """
    if not os.path.exists(DOCS_DIR):
        raise FileNotFoundError(f"El directorio {DOCS_DIR} no existe.")

    all_docs = []
    
    # Recorrer todos los archivos en docs/
    for filename in os.listdir(DOCS_DIR):
        file_path = os.path.join(DOCS_DIR, filename)
        
        if filename.endswith(".pdf"):
            print(f"📄 Cargando PDF: {filename}...")
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            all_docs.extend(docs)
        elif filename.endswith(".csv"):
            print(f"📊 Cargando CSV: {filename}...")
            # Usar CSVLoader para cargar los datos fila por fila
            loader = CSVLoader(file_path=file_path, encoding='utf-8')
            docs = loader.load()
            all_docs.extend(docs)
            
    if not all_docs:
        print("⚠️ No se encontraron documentos válidos (PDF/CSV) en la carpeta docs.")
        return []

    print(f"✂️ Dividiendo {len(all_docs)} páginas en chunks...")
    
    # Dividir el texto
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    chunks = text_splitter.split_documents(all_docs)
    print(f"✅ Se generaron {len(chunks)} fragmentos (chunks).")
    
    return chunks
