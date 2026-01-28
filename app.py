from flask import Flask, render_template, request, redirect, url_for
import redis
import json
import uuid
from datetime import datetime
from scanner import VulnerabilityScanner

app = Flask(__name__)

# CONFIGURATION REDIS : L'erreur 'invalid username-password pair' vient d'ici
# Assure-toi que ce mot de passe est EXACTEMENT le même que dans ton docker-compose.yml
r = redis.Redis(
    host='redis', 
    port=6379, 
    password='pass123', # 
    decode_responses=True
)

scanner = VulnerabilityScanner()

@app.route('/')
def index():
    try:
        # Récupération sécurisée des données dans Redis
        keys = r.keys("scan:*")
        scans = []
        for k in keys:
            val = r.get(k)
            if val:
                scans.append(json.loads(val))
        
        # Tri chronologique
        scans.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        total_scans = len(scans)
        # On cherche 'Alerte' au lieu de l'emoji pour éviter les bugs de caractères
        vulnerabilities = len([s for s in scans if "Alerte" in s['result']])
        
        # Calcul du score de santé
        health_score = 100
        if total_scans > 0:
            health_score = int(((total_scans - vulnerabilities) / total_scans) * 100)

        return render_template('index.html', 
                               scans=scans, 
                               total=total_scans, 
                               alerts=vulnerabilities, 
                               health=health_score)
    except Exception as e:
        # Message d'erreur détaillé pour le debug
        return f"Erreur Base de donnees : {e}", 500

@app.route('/scan', methods=['POST'])
def scan_code():
    code_content = request.form.get('code')
    if code_content:
        # Appel au moteur de scan
        res = scanner.scan(code_content)
        
        # Génération d'un ID unique pour ne pas écraser les anciens scans
        s_id = str(uuid.uuid4())
        data = {
            'id': s_id, 
            'code': code_content, 
            'result': res, 
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Stockage JSON dans Redis
        r.set(f"scan:{s_id}", json.dumps(data))
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Le host 0.0.0.0 est obligatoire pour Docker
    app.run(host='0.0.0.0', port=5000, debug=False)