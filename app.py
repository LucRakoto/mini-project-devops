from flask import Flask, render_template_string, request, redirect, url_for
from redis import Redis

app = Flask(__name__)
# On se connecte à Redis (le nom du service dans docker-compose)
db = Redis(host='redis', port=6379, decode_responses=True)

# Interface HTML simple intégrée
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Ma Liste des taches</title></head>
<body>
    <h1>Ma Liste de Tâches CRUD</h1>
    <form action="/add" method="POST">
        <input type="text" name="task" placeholder="Nouvelle tâche..." required>
        <button type="submit">Ajouter une tache</button>
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
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        db.rpush('tasks', task)
    return redirect(url_for('index'))

@app.route('/delete/<task>')
def delete(task):
    db.lrem('tasks', 0, task)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)