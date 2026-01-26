import os
from flask import Flask, render_template_string
from redis import Redis

app = Flask(__name__)
db = Redis(host='redis', port=6379, decode_responses=True)

# On récupère le titre depuis l'environnement
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
    # On passe bien 'title' et 'tasks' au template
    return render_template_string(HTML_TEMPLATE, tasks=tasks, title=app_title)

# ... (garde tes routes /add et /delete comme elles étaient)