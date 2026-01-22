from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>bon   jour 2</h1>"

if __name__ == "__main__":
    # debug=True permet à Flask de redémarrer dès que tu sauvegardes
    app.run(host='0.0.0.0', port=5000, debug=True)