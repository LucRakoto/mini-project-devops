import os
import json
import uuid
import redis
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from scanner import VulnerabilityScanner

app = Flask(__name__)

# --- CONFIGURATION LOGS BLUE TEAM ---
# On centralise tout sur app.logger pour être propre avec Flask
log_handler = RotatingFileHandler('audit.log', maxBytes=100000, backupCount=3)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - IP: %(client_ip)s - %(message)s')
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.INFO)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

# --- VARIABLES D'ENVIRONNEMENT ---
R_PASS = os.getenv('REDIS_PASSWORD', 'pass123')

# --- INITIALISATION ---
try:
    r = redis.Redis(
        host='redis', 
        port=6379, 
        password=R_PASS, 
        decode_responses=True
    )
    scanner = VulnerabilityScanner()
except Exception as e:
    app.logger.error(f"Erreur d'initialisation : {e}", extra={'client_ip': 'SYSTEM'})

@app.before_request
def log_request_info():
    # On prépare l'IP pour le formateur de log
    # request.remote_addr récupère l'IP de celui qui visite le site
    extra_data = {'client_ip': request.remote_addr}
    if request.path != '/static/': # Évite de logger les fichiers CSS/Images pour rien
        app.logger.info(f"ACCESS_PATH: {request.path}", extra=extra_data)

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
        critique = "Alerte" # On simplifie ici
        fails = len([s for s in scans if critique in s['result']])
        
        health = 100
        if total > 0:
            health = int(((total - fails) / total) * 100)

        return render_template('index.html', 
                               scans=scans, 
                               total=total, 
                               alerts=fails, 
                               health=health)
    except Exception as e:
        app.logger.error(f"Database Error: {e}", extra={'client_ip': request.remote_addr})
        return f"Database Error: {e}", 500

@app.route('/scan', methods=['POST'])
def scan_code():
    content = request.form.get('code')
    if content:
        # Action Blue Team : Loguer le contenu du scan
        # On limite l'affichage du contenu à 50 caractères dans les logs pour la lisibilité
        app.logger.info(f"SCAN_START - Content: {content[:50]}...", extra={'client_ip': request.remote_addr})
        
        res = scanner.scan(content)
        s_id = str(uuid.uuid4())
        
        data = {
            'id': s_id, 
            'code': content, 
            'result': res, 
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Si une alerte est détectée, on logue un WARNING pour la Blue Team
        if "Alerte" in res:
            app.logger.warning(f"SECURITY_ALERT - VULNERABILITY_FOUND", extra={'client_ip': request.remote_addr})
            
        r.set(f"scan:{s_id}", json.dumps(data))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    