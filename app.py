import os, json
from flask import Flask, render_template, request, redirect, url_for
from redis import Redis
from datetime import datetime
from scanner import VulnerabilityScanner # On importe ton nouveau module !

app = Flask(__name__)
db = Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379, password=os.getenv('REDIS_PASSWORD'), decode_responses=True)
ia_scanner = VulnerabilityScanner() # On initialise l'IA

@app.route('/')
def index():
    raw_data = db.lrange('scans', 0, -1)
    reports = [json.loads(r) for r in raw_data]
    return render_template('index.html', reports=reports) # On utilise un vrai fichier HTML !

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.form.get('code_snippet')
    if code:
        result = ia_scanner.scan(code) # L'IA travaille ici
        db.rpush('scans', json.dumps({
            "preview": code[:30], 
            "result": result,
            "date": datetime.now().strftime("%H:%M:%S")
        }))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)