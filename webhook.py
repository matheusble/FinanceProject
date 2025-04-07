from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

@app.route("/github-webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        try:
            repo_path = "/home/Finance"
            os.chdir(repo_path)

            subprocess.run(["git", "pull", "origin", "main"], check=True)

            subprocess.run(["/home/Finance/venv/bin/pip", "install", "-r", "requirements.txt"], check=True)

            subprocess.run(["systemctl", "restart", "minha_api.service"], check=True)

            return "Atualização concluída!", 200
        except Exception as e:
            return str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

