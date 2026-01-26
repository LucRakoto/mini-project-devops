import os
from flask import Flask, render_template_string, request, redirect, url_for
from redis import Redis

app = Flask(__name__)
# Connexion à Redis
db = Redis(host='redis', port=6379, decode_responses=True)

# Variable d'environnement pour le titre
app_title = os.getenv('APP_TITLE', 'Ma Liste de Tâches')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ title }}</h1>
    <form action="/add" method="POST">
        <input type="text" name="task" placeholder="Nouvelle tâche..." required>
        <button type="submit">Ajouter</button>
    </form>
    <ul>
        {% for task in tasks %}
            <li>{{ task }} <a href="/delete/{{ task }}">[Supprimer]</a></li>
        {% endfor %}
    </ul>
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