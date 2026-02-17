import json
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

SCORE_FILE = "scores.json"

# ファイルなければ作る
if not os.path.exists(SCORE_FILE):
    with open(SCORE_FILE, "w") as f:
        json.dump([], f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit_score", methods=["POST"])
def submit_score():
    data = request.json

    with open(SCORE_FILE, "r") as f:
        scores = json.load(f)

    scores.append({'name': data['name'], 'score': data['score']})
    scores.sort(key=lambda x: x['score'], reverse=True)

    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f)

    return jsonify({'status': 'ok'})

@app.route("/highscore")
def highscore():
    with open(SCORE_FILE, "r") as f:
        scores = json.load(f)

    return render_template("highscore.html", scores=scores[:3])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

