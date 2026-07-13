# Usa una imagen oficial de Python ligera
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema operativo que puedan ser necesarias para FAISS o compilar paquetes
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos de requerimientos primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código del proyecto al contenedor
COPY . .

# Expone el puerto que usa FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "server.py"]
