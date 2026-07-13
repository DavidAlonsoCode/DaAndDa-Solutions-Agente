from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from .vector_store import load_index
from src.config import BASE_DIR
import os

# Ruta a la base de datos local de SQLite
db_path = os.path.join(BASE_DIR, "chat_history.db")
db_uri = f"sqlite:///{db_path}"

def get_session_history(session_id: str):
    """Obtiene o crea el historial de mensajes de una sesión en la base de datos."""
    return SQLChatMessageHistory(
        session_id=session_id,
        connection=db_uri
    )

def get_llm():
    """Retorna la instancia del modelo de lenguaje (Gemini)."""
    return ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        temperature=0.2
    )

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Variable global para cachear la cadena y no recrearla en cada request
_rag_chain = None

def get_agent():
    """Configura y retorna la cadena RAG completa usando LCEL y Memoria."""
    global _rag_chain
    if _rag_chain is not None:
        return _rag_chain

    # 1. Cargar el Vector Store
    vectorstore = load_index()
    if vectorstore is None:
        raise FileNotFoundError("No se encontró el índice FAISS. Debes ejecutar ingest.py primero.")
        
    # Crear el retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    
    # 2. Configurar el LLM
    llm = get_llm()
    
    # 3. Leer qué archivos hay disponibles para que la IA sepa su alcance real
    docs_dir = os.path.join(BASE_DIR, "docs")
    archivos_disponibles = "Ninguno"
    if os.path.exists(docs_dir):
        archivos_disponibles = ", ".join([f for f in os.listdir(docs_dir) if f.endswith(('.pdf', '.txt', '.csv'))])

    # 4. Prompt que acepta historial
    system_prompt = (
        "Eres un asistente experto de inteligencia artificial (Nivel Staff Engineer) para los ingenieros de Da&Da Solutions. "
        "Tu objetivo es responder preguntas técnicas sobre la arquitectura, código y políticas de la empresa de forma clara, profesional y muy precisa.\n\n"
        f"Actualmente tienes acceso a la siguiente base de conocimiento (archivos): {archivos_disponibles}.\n"
        "Si el usuario te saluda, te pregunta en qué puedes ayudarle, o qué sabes hacer, preséntate amablemente y dale "
        "un breve resumen integrado de máximo dos o tres líneas explicando de qué tratan en conjunto los documentos que tienes disponibles, "
        "para que sepa exactamente qué puede consultarte. No listes los archivos uno por uno, solo resume la temática global basada en sus nombres.\n\n"
        "Para otras consultas técnicas, utiliza EXCLUSIVAMENTE los siguientes fragmentos de contexto recuperado para responder a la pregunta. "
        "Si la respuesta no está en el contexto, di claramente 'No tengo información sobre eso en los documentos actuales' "
        "y no intentes inventar una respuesta. Nunca menciones explícitamente que estás leyendo un 'contexto' o 'documento'.\n\n"
        "Contexto:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
    
    # 4. Construir la cadena principal
    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | prompt
        | llm
        | StrOutputParser()
    )
    
    rag_chain = RunnableParallel(
        {
            "context": lambda x: retriever.invoke(x["input"]), 
            "input": lambda x: x["input"],
            "chat_history": lambda x: x.get("chat_history", [])
        }
    ).assign(answer=rag_chain_from_docs)
    
    # 5. Envolver con historial de mensajes
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
    
    _rag_chain = conversational_rag_chain
    return _rag_chain
