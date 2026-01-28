# ÉTAPE 1 : La construction (le constructeur)
FROM python:3.9-slim AS builder

WORKDIR /app
COPY requirements.txt .
# On installe les dépendances
RUN pip install --user --no-cache-dir -r requirements.txt

# ÉTAPE 2 : L'image finale (le coureur)
FROM python:3.9-slim

WORKDIR /app

# 1. On récupère les bibliothèques installées
COPY --from=builder /root/.local /root/.local

# 2. MODIFICATION ICI : On copie TOUT le projet (app.py, scanner.py, templates/)
# Le premier "." est ton dossier sur ton PC, le second "." est le dossier /app dans Docker
COPY . . 

# On s'assure que Python trouve nos bibliothèques
ENV PATH=/root/.local/bin:$PATH
# On force Python à afficher les logs en temps réel (pratique pour le débug)
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]