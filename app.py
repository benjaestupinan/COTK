import json
import os
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder=".", static_url_path="")
DATA_FILE = "/tmp/data.json"


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"names": [], "scores": {}}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


@app.route("/api/data")
def get_data():
    return jsonify(load_data())


@app.route("/api/increment", methods=["POST"])
def increment():
    data = load_data()
    name = request.json.get("name")
    password = request.json.get("password")

    if password != "pepito123":
        return jsonify({"error": "Contraseña incorrecta"}), 401

    if name in data["scores"]:
        data["scores"][name] += 1
    else:
        data["scores"][name] = 1
        data["names"].append(name)

    save_data(data)
    return jsonify({"score": data["scores"][name]})


@app.route("/api/add", methods=["POST"])
def add_name():
    data = load_data()
    name = request.json.get("name")
    password = request.json.get("password")

    if password != "pepito123":
        return jsonify({"error": "Contraseña incorrecta"}), 401

    if not name:
        return jsonify({"error": "Nombre requerido"}), 400

    if name in data["names"]:
        return jsonify({"error": "Nombre ya existe"}), 400

    data["names"].append(name)
    data["scores"][name] = 0
    save_data(data)
    return jsonify({"success": True})


@app.route("/<path:path>")
def serve(path=""):
    from flask import send_from_directory

    if path == "" or path == "index.html":
        return send_from_directory(".", "index.html")
    return send_from_directory(".", path)


# Vercel entrypoint
app = app
