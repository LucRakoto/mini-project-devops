import os
import json
import uuid
import redis
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from scanner import VulnerabilityScanner

app = Flask(__name__)

# Utilisation des variables d'environnement pour securiser le code
REDIS_PASS = os.getenv('REDIS_PASSWORD', 'pass123')

try:
    r = redis.Redis(
        host='redis', 
        port=6379, 
        password=REDIS_PASS, 
        decode_responses=True
    )
    scanner = VulnerabilityScanner()
except Exception as e:
    print(f"Erreur de configuration : {e}")

@app.route('/')
def index():
    try:
        keys = r.keys("scan:*")
        scans = [json.loads(r.get(k)) for k in keys]
        scans.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        total_scans = len(scans)
        vulnerabilities = len([s for s in scans if "Alerte" in s['result']])
        health_score = 100 if total_scans == 0 else int(((total_scans - vulnerabilities) / total_scans) * 100)

        return render_template('index.html', scans=scans, total=total_scans, alerts=vulnerabilities, health=health_score)
    except Exception as e:
        return f"Connexion impossible : {e}", 500

@app.route('/scan', methods=['POST'])
def scan_code():
    code_content = request.form.get('code')
    if code_content:
        res = scanner.scan(code_content)
        s_id = str(uuid.uuid4())
        data = {
            'id': s_id, 
            'code': code_content, 
            'result': res, 
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        r.set(f"scan:{s_id}", json.dumps(data))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)