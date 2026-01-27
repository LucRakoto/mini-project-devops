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
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; padding: 50px; }
        .container { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 100%; max-width: 500px; }
        h1 { color: #1c1e21; margin-top: 0; }
        form { display: flex; gap: 10px; margin-bottom: 20px; }
        input[type="text"] { flex-grow: 1; padding: 10px; border: 1px solid #ddd; border-radius: 6px; outline: none; }
        button { background-color: #1877f2; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; }
        button:hover { background-color: #166fe5; }
        ul { list-style: none; padding: 0; }
        li { background: #fff; margin-bottom: 8px; padding: 12px; border-radius: 6px; border: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
        .delete-btn { color: #ff4d4d; text-decoration: none; font-size: 0.8em; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ title }}</h1>
        
        <form action="/add" method="POST">
            <input type="text" name="task" placeholder="Quelle est la prochaine étape ?" required>
            <button type="submit">Ajouter</button>
        </form>

        <ul>
            {% for task in tasks %}
                <li>
                    <span>{{ task }}</span>
                    <a href="/delete/{{ task }}" class="delete-btn">Supprimer</a>
                </li>
            {% endfor %}
        </ul>
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