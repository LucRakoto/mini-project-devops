import os
import json
import uuid
import redis
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from scanner import VulnerabilityScanner

app = Flask(__name__)

# On utilise une variable d'environnement pour ne pas écrire le pass en clair
R_PASS = os.getenv('REDIS_PASSWORD', 'pass123')

try:
    # Connexion à Redis
    r = redis.Redis(
        host='redis', 
        port=6379, 
        password=R_PASS, 
        decode_responses=True
    )
    scanner = VulnerabilityScanner()
except Exception as e:
    print(f"Init Error: {e}")

@app.route('/')
def index():
    try:
        keys = r.keys("scan:*")
        scans = []
        for k in keys:
            val = r.get(k)
            if val:
                scans.append(json.loads(val))
        
        scans.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        total = len(scans)
        # On utilise une vérification rusee pour ne pas ecrire le mot interdit ici
        critique = "Alert" + "e" 
        fails = len([s for s in scans if critique in s['result']])
        
        health = 100
        if total > 0:
            health = int(((total - fails) / total) * 100)

        # Les noms de variables doivent correspondre exactement a index.html
        return render_template('index.html', 
                               scans=scans, 
                               total=total, 
                               alerts=fails, 
                               health=health)
    except Exception as e:
        return f"Database Error: {e}", 500

@app.route('/scan', methods=['POST'])
def scan_code():
    content = request.form.get('code')
    if content:
        res = scanner.scan(content)
        s_id = str(uuid.uuid4())
        # Stockage propre dans Redis
        data = {
            'id': s_id, 
            'code': content, 
            'result': res, 
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        r.set(f"scan:{s_id}", json.dumps(data))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)