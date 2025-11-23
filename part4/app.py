from flask import Flask, send_from_directory
from flask_restx import Api
from app.api.auth import api as auth_ns

app = Flask(__name__, static_folder="part4/base_files")
app.config["JWT_SECRET_KEY"] = "secret-key"

api = Api(app)
api.add_namespace(auth_ns, path="/api/v1/auth")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/login.html")
def login():
    return send_from_directory(app.static_folder, "login.html")

if __name__ == "__main__":
    app.run(debug=True)
