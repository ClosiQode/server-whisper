FROM python:3.9-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers nécessaires
COPY requirements.txt .
COPY server_faster_whisper.py .
COPY client.html .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposition du port
EXPOSE 5000

# Commande de démarrage
CMD ["python", "server_faster_whisper.py", "--model", "tiny", "--host", "0.0.0.0", "--port", "5000"]
