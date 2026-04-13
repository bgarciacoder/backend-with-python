from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
import uuid

from src.db import mongo
from src.middleware.api_key_required import api_key_required
from utils.token_utils import store_token
from src.middleware.jwt_required import jwt_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# =========================
# REGISTER
# =========================
@auth_bp.route("/register", methods=["POST"])
@api_key_required
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        return jsonify({"error": "Missing fields"}), 400

    if mongo.db.users.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 409

    hashed_password = generate_password_hash(password)

    mongo.db.users.insert_one({
        "username": username,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    })

    return jsonify({"message": "User created successfully"}), 201


# =========================
# LOGIN
# =========================
@auth_bp.route("/login", methods=["POST"])
@api_key_required
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing credentials"}), 400

    user = mongo.db.users.find_one({"email": email})

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    jti = str(uuid.uuid4())
    expires = datetime.utcnow() + timedelta(hours=24)

    payload = {
        "jti": jti,
        "user_id": str(user["_id"]),
        "exp": expires,
        "iat": datetime.utcnow()
    }

    token = jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256"
    )

    # Guardar sesión en DB
    store_token(
        jti=jti,
        user_id=str(user["_id"]),
        user_agent=request.headers.get("User-Agent"),
        ip=request.remote_addr
    )

    return jsonify({
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"]
        }
    }), 200


@auth_bp.route("/me", methods=["GET"])
@api_key_required
@jwt_required
def get_me(payload):
    return {"user_id": payload["sub"]}, 200