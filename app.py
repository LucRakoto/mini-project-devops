import os
from flask import Flask, render_template_string, request, redirect, url_for
from redis import Redis
import json
from datetime import datetime

app = Flask(__name__)

# Connexion à Redis via variables d'environnement
redis_pass = os.getenv('REDIS_PASSWORD')
db = Redis(
    host=os.getenv('REDIS_HOST', 'redis'), 
    port=6379, 
    password=redis_pass, 
    decode_responses=True
)

app_title = os.getenv('APP_TITLE', 'Ma Liste de Tâches')

# Le template avec CSS, Formulaire et Liste intégrés
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #f4f7f6; display: flex; justify-content: center; padding: 40px; }
        .card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); width: 100%; max-width: 450px; }
        h1 { color: #2d3436; margin-bottom: 25px; font-size: 24px; }
        .input-group { display: flex; gap: 10px; margin-bottom: 25px; }
        input[type="text"] { flex-grow: 1; padding: 12px; border: 2px solid #dfe6e9; border-radius: 8px; outline: none; transition: 0.3s; }
        input[type="text"]:focus { border-color: #0984e3; }
        button { background-color: #0984e3; color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-weight: bold; }
        button:hover { background-color: #74b9ff; }
        ul { list-style: none; padding: 0; }
        li { background: #fff; margin-bottom: 10px; padding: 15px; border-radius: 8px; border: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }
        .delete-btn { color: #d63031; text-decoration: none; font-weight: bold; font-size: 14px; }
        .delete-btn:hover { color: #ff7675; }
    </style>
</head>
<body>
    <div class="card">
        <h1>{{ title }}</h1>
        
        <form action="/add" method="POST" class="input-group">
            <input type="text" name="task" placeholder="Que faut-il faire ?" required>
            <button type="submit">Ajouter</button>
        </form>

       <ul>
            {% for task in tasks %}
                <li>
                    <div>
                        <strong>{{ task.content }}</strong> <br>
                        <small style="color: #636e72;">Ajouté le : {{ task.date }}</small>
                    </div>
                    <a href="/delete/{{ task.content }}" class="delete-btn">Supprimer</a>
                </li>
            {% endfor %}
       </ul>
    </div>
</body>
</html>
'''
@app.route('/')
def index():
    raw_tasks = db.lrange('tasks', 0, -1)
    tasks = []
    for item in raw_tasks:
        tasks.append(json.loads(item)) # On retransforme le texte en objet Python
    return render_template_string(HTML_TEMPLATE, tasks=tasks, title=app_title)

@app.route('/add', methods=['POST'])
def add():
    task_text = request.form.get('task')
    if task_text:
        # On crée un dictionnaire (objet) avec le texte et la date
        task_data = {
            "content": task_text,
            "date": datetime.now().strftime("%d/%m %H:%M") # Format: Jour/Mois Heure:Min
        }
        # On transforme l'objet en texte JSON pour Redis
        db.rpush('tasks', json.dumps(task_data))
    return redirect(url_for('index'))

@app.route('/delete/<task>')
def delete(task):
    db.lrem('tasks', 1, task)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)