import os, json
from flask import Flask, render_template_string, request, redirect, url_for
from redis import Redis
from datetime import datetime

app = Flask(__name__)
db = Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379, 
           password=os.getenv('REDIS_PASSWORD'), decode_responses=True)

# --- NOTRE SIMULATION D'IA ---
def analyze_code(code):
    issues = []
    if "password" in code.lower(): issues.append("Password Leak")
    if "eval(" in code.lower(): issues.append("Code Injection")
    return "SAFE" if not issues else f"VULNERABLE: {', '.join(issues)}"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>CyberScan IA</title>
    <style>
        body { font-family: 'Courier New', monospace; background-color: #0d1117; color: #c9d1d9; padding: 40px; }
        .container { background: #161b22; padding: 25px; border-radius: 8px; border: 1px solid #30363d; max-width: 700px; margin: auto; }
        h1 { color: #58a6ff; }
        textarea { width: 100%; height: 100px; background: #0d1117; color: #a5d6ff; border: 1px solid #30363d; border-radius: 5px; padding: 10px; margin-bottom: 10px; }
        button { background: #238636; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; }
        .result { font-size: 0.8em; color: #8b949e; }
        .status { font-weight: bold; color: #ff7b72; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 CyberScan CI/CD</h1>
        <form action="/analyze" method="POST">
            <textarea name="code_snippet" placeholder="Collez le code à analyser ici..." required></textarea>
            <button type="submit">Lancer l'Analyse IA</button>
        </form>
        <hr style="border: 0.5px solid #30363d; margin: 20px 0;">
        <ul>
            {% for report in reports %}
                <li>
                    <strong>Code:</strong> {{ report.preview }}... <br>
                    <span class="status">Résultat: {{ report.result }}</span> <br>
                    <span class="result">Date: {{ report.date }}</span>
                </li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    raw_data = db.lrange('scans', 0, -1)
    reports = [json.loads(r) for r in raw_data]
    return render_template_string(HTML_TEMPLATE, reports=reports)

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.form.get('code_snippet')
    if code:
        result = analyze_code(code) # Appel de notre "IA"
        data = {
            "preview": code[:30], 
            "result": result,
            "date": datetime.now().strftime("%H:%M:%S")
        }
        db.rpush('scans', json.dumps(data))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)