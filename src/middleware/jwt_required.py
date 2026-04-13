import jwt
from functools import wraps
from flask import request, jsonify, current_app
from utils.token_utils import is_token_revoked

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth = request.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer "):
            return jsonify({"error": "Token required"}), 401

        token = auth.split(" ")[1]

        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        if is_token_revoked(payload):
            return jsonify({"error": "Token revoked"}), 401

        return f(payload, *args, **kwargs)

    return decorated