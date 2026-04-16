from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
BIN_ID = "69e03278856a6821893b6c1d"


@app.route("/api/data")
def get_data():
    try:
        res = requests.get(f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest")
        if res.status_code != 200:
            return jsonify({"names": [], "scores": {}})
        record = res.json().get("record")
        if not record:
            return jsonify({"names": [], "scores": {}})
        return jsonify(
            {"names": record.get("names", []), "scores": record.get("scores", {})}
        )
    except Exception:
        return jsonify({"names": [], "scores": {}})


@app.route("/api/increment", methods=["POST"])
def increment():
    try:
        data = request.json or {}
        name = data.get("name")
        password = data.get("password")

        if password != "pepito123":
            return jsonify({"error": "Contraseña incorrecta"}), 401

        res = requests.get(f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest")
        if res.status_code != 200:
            return jsonify({"error": "Error al leer"}), 500

        record = res.json().get("record", {"names": [], "scores": {}})
        scores = record.get("scores", {})
        names = record.get("names", [])

        if name in scores:
            scores[name] += 1
        else:
            scores[name] = 1
            names.append(name)

        requests.put(
            f"https://api.jsonbin.io/v3/b/{BIN_ID}",
            json={"names": names, "scores": scores},
            headers={"Content-Type": "application/json"},
        )

        return jsonify({"score": scores[name]})
    except Exception:
        return jsonify({"error": "Error del servidor"}), 500


@app.route("/api/add", methods=["POST"])
def add_name():
    try:
        data = request.json or {}
        name = data.get("name")

        if not name:
            return jsonify({"error": "Nombre requerido"}), 400

        res = requests.get(f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest")
        if res.status_code != 200:
            return jsonify({"error": "Error al leer"}), 500

        record = res.json().get("record", {"names": [], "scores": {}})
        names = record.get("names", [])

        if name in names:
            return jsonify({"error": "Nombre ya existe"}), 400

        names.append(name)
        scores = record.get("scores", {})
        scores[name] = 0

        requests.put(
            f"https://api.jsonbin.io/v3/b/{BIN_ID}",
            json={"names": names, "scores": scores},
            headers={"Content-Type": "application/json"},
        )

        return jsonify({"success": True})
    except Exception:
        return jsonify({"error": "Error del servidor"}), 500


@app.route("/")
def index():
    from flask import send_from_directory

    return send_from_directory(".", "index.html")


@app.route("/<path:filename>")
def files(filename):
    from flask import send_from_directory

    return send_from_directory(".", filename)
