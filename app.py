import os
from flask import Flask, render_template_string, request, redirect, url_for
from redis import Redis

app = Flask(__name__)
# Connexion à Redis
redis_pass = os.getenv('REDIS_PASSWORD') # Récupère le secret

db = Redis(
    host=os.getenv('REDIS_HOST', 'redis'), 
    port=6379, 
    password=redis_pass,  # Utilise le secret ici
    decode_responses=True
)

# Variable d'environnement pour le titre
app_title = os.getenv('APP_TITLE', 'Ma Liste de Tâches')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 50px; }
        .container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        li { margin-bottom: 10px; padding: 5px; border-bottom: 1px solid #eee; }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ title }}</h1>
        </div>
</body>
</html>
'''

@app.route('/')
def index():
    tasks = db.lrange('tasks', 0, -1)
    return render_template_string(HTML_TEMPLATE, tasks=tasks, title=app_title)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        db.rpush('tasks', task)
    return redirect(url_for('index'))

@app.route('/delete/<task>')
def delete(task):
    db.lrem('tasks', 1, task)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # On lance l'app sur le port 5000
    app.run(host='0.0.0.0', port=5000)