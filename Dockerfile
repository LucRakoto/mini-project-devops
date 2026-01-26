# ÉTAPE 1 : La construction (le constructeur)
FROM python:3.9-slim AS builder

WORKDIR /app
COPY requirements.txt .
# On installe les dépendances dans un dossier local
RUN pip install --user --no-cache-dir -r requirements.txt

# ÉTAPE 2 : L'image finale (le coureur)
FROM python:3.9-slim

WORKDIR /app
# On récupère seulement ce qui est nécessaire depuis l'étape précédente
COPY --from=builder /root/.local /root/.local
COPY app.py .

# On s'assure que Python trouve nos bibliothèques
ENV PATH=/root/.local/bin:$PATH

CMD ["python", "app.py"]