from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


@app.route("/api/data")
def get_data():
    res = requests.get(
        "https://api.jsonbin.io/v3/b/69e03278856a6821893b6c1d/latest", timeout=5
    )
    record = res.json().get("record") if res.status_code == 200 else None
    if not record:
        return jsonify({"names": [], "scores": {}})
    if "scores" not in record:
        record["scores"] = {}
    if "names" not in record:
        record["names"] = []
    return jsonify(record)


@app.route("/api/increment", methods=["POST"])
def increment():
    data = request.json or {}
    name = data.get("name")
    password = data.get("password")

    if password != "pepito123":
        return jsonify({"error": "Contraseña incorrecta"}), 401

    res = requests.get(
        "https://api.jsonbin.io/v3/b/69e03278856a6821893b6c1d/latest", timeout=5
    )
    record = res.json().get("record") if res.status_code == 200 else None

    if not record:
        record = {"names": [], "scores": {}}

    if "scores" not in record:
        record["scores"] = {}
    if "names" not in record:
        record["names"] = []

    if name in record["scores"]:
        record["scores"][name] += 1
    else:
        record["scores"][name] = 1
        record["names"].append(name)

    requests.put(
        "https://api.jsonbin.io/v3/b/69e03278856a6821893b6c1d",
        json=record,
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    return jsonify({"score": record["scores"][name]})


@app.route("/api/add", methods=["POST"])
def add_name():
    data = request.json or {}
    name = data.get("name")

    if not name:
        return jsonify({"error": "Nombre requerido"}), 400

    res = requests.get(
        "https://api.jsonbin.io/v3/b/69e03278856a6821893b6c1d/latest", timeout=5
    )
    record = res.json().get("record") if res.status_code == 200 else None

    if not record:
        record = {"names": [], "scores": {}}

    if "scores" not in record:
        record["scores"] = {}
    if "names" not in record:
        record["names"] = []

    if name in record["names"]:
        return jsonify({"error": "Nombre ya existe"}), 400

    record["names"].append(name)
    record["scores"][name] = 0

    requests.put(
        "https://api.jsonbin.io/v3/b/69e03278856a6821893b6c1d",
        json=record,
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    return jsonify({"success": True})


@app.route("/")
def index():
    from flask import send_from_directory

    return send_from_directory(".", "index.html")


@app.route("/<path:filename>")
def files(filename):
    from flask import send_from_directory

    return send_from_directory(".", filename)
