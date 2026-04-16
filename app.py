import json
import requests
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

BIN_ID = "69e03278856a6821893b6c1d"
BASE_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"


def load_data():
    try:
        res = requests.get(BASE_URL, timeout=5)
        if res.status_code == 200:
            data = res.json().get("record")
            if data:
                return data
        return {"names": [], "scores": {}}
    except Exception as e:
        print(f"load_data error: {e}")
        return {"names": [], "scores": {}}


def save_data(data):
    try:
        headers = {"Content-Type": "application/json"}
        res = requests.put(BASE_URL, headers=headers, json=data, timeout=5)
        print(f"save_data response: {res.status_code}")
        return res
    except Exception as e:
        print(f"save_data error: {e}")


@app.route("/api/data")
def get_data():
    print("get_data called")
    data = load_data()
    print(f"Returning: {data}")
    return jsonify(data)


@app.route("/api/ping")
def ping():
    return jsonify({"pong": True})


@app.route("/api/increment", methods=["POST"])
def increment():
    data = load_data()
    name = request.json.get("name")
    password = request.json.get("password")

    print(f"Increment: name={name}, data={data}")

    if password != "pepito123":
        return jsonify({"error": "Contraseña incorrecta"}), 401

    if name in data["scores"]:
        data["scores"][name] += 1
    else:
        data["scores"][name] = 1
        data["names"].append(name)

    save_data(data)
    print(f"After save: {data}")
    return jsonify({"score": data["scores"][name]})


@app.route("/api/add", methods=["POST"])
def add_name():
    data = load_data()
    name = request.json.get("name")
    password = request.json.get("password")

    print(f"Add: name={name}, data={data}")

    if password != "pepito123":
        return jsonify({"error": "Contraseña incorrecta"}), 401

    if not name:
        return jsonify({"error": "Nombre requerido"}), 400

    if name in data["names"]:
        return jsonify({"error": "Nombre ya existe"}), 400

    data["names"].append(name)
    data["scores"][name] = 0
    save_data(data)
    print(f"After add: {data}")
    return jsonify({"success": True})


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/<path:filename>")
def files(filename):
    return send_from_directory(".", filename)


# Vercel entrypoint
app = app
