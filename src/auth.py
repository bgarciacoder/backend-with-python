# auth.py
from flask import request, jsonify
from settings import API_AUTH_TOKEN

def token_required(f):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token required"}), 401

        token = auth_header.split(" ")[1]
        if token != API_AUTH_TOKEN:
            return jsonify({"error": "Invalid Token"}), 403

        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__  # para que Flask no se queje
    return wrapper