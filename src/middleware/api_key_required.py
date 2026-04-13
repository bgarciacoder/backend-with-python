from functools import wraps
from flask import request, jsonify, current_app

def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing"}), 401

        token = auth_header.split(" ")[1]

        if token != current_app.config["API_KEY"]:
            return jsonify({"error": "Invalid API token"}), 403

        return f(*args, **kwargs)

    return decorated