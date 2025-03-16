FROM python:3.9-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers nécessaires
COPY requirements.txt .
COPY server_faster_whisper.py .
COPY documentation.html .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Création des répertoires pour les volumes
RUN mkdir -p /app/config /app/models

# Exposition du port
EXPOSE 5000

# Commande par défaut (utilise les variables d'environnement)
CMD ["python", "server_faster_whisper.py"]
