from flask import Flask, render_template, request, redirect, url_for
import redis
import json
import uuid
from datetime import datetime
from scanner import VulnerabilityScanner

app = Flask(__name__)

# Connexion à Redis (Assure-toi que les identifiants correspondent à ton docker-compose)
r = redis.Redis(host='redis', port=6379, password='votre_mot_de_passe_robuste', decode_responses=True)

scanner = VulnerabilityScanner()

@app.route('/')
def index():
    try:
        # 1. Récupération de tous les scans stockés
        keys = r.keys("scan:*")
        scans = []
        for k in keys:
            data = r.get(k)
            if data:
                scans.append(json.loads(data))
        
        # 2. Tri par date (du plus récent au plus ancien)
        scans.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        # 3. Calcul des statistiques pour le Dashboard
        total_scans = len(scans)
        vulnerabilities = len([s for s in scans if "❌" in s['result']])
        
        # Calcul du score de santé (sur 100)
        health_score = 100
        if total_scans > 0:
            health_score = int(((total_scans - vulnerabilities) / total_scans) * 100)

        return render_template('index.html', 
                               scans=scans, 
                               total=total_scans, 
                               alerts=vulnerabilities,
                               health=health_score)
    except Exception as e:
        return f"Erreur de connexion à la base de données : {e}", 500

@app.route('/scan', method=['POST'])
def scan_code():
    code_content = request.form.get('code')
    if not code_content:
        return redirect(url_for('index'))

    # Analyse du code via le scanner
    result = scanner.scan(code_content)
    
    # Création de l'objet de scan pour Redis
    scan_id = str(uuid.uuid4())
    scan_data = {
        'id': scan_id,
        'code': code_content,
        'result': result,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Sauvegarde dans Redis avec une expiration (optionnel)
    r.set(f"scan:{scan_id}", json.dumps(scan_data))
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)