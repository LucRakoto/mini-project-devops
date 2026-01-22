# On utilise une version légère de Python
FROM python:3.9-slim

# On définit le dossier où le code va vivre dans le conteneur
WORKDIR /app

# On copie le fichier requirements.txt de ton PC vers le conteneur
COPY requirements.txt .

# On installe Flask (Docker va lire le fichier requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# On copie le reste de tes fichiers (app.py) dans le conteneur
COPY . .

# On expose le port 5000 (celui utilisé par Flask)
EXPOSE 5000

# La commande pour démarrer l'application
CMD ["python", "app.py"]