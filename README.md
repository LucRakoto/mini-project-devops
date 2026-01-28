#  CyberScan IA - Static Analysis Tool

Ce projet est un outil de **Security Scanning (SAST)** automatisé permettant de détecter des vulnérabilités dans le code source Python.

## Fonctionnalités
* **Analyse en temps réel** : Interface web Flask pour tester des snippets de code.
* **Persistance** : Historique des scans stocké sous Redis.
* **CI/CD Security** : Pipeline GitHub Actions qui bloque les commits contenant des failles (SQLi, XSS, Secrets).

## Installation (Docker)
1. Clonez le dépôt.
2. Lancez l'infrastructure :
   ```bash
   docker-compose up --build