from flask import Blueprint, jsonify, request
from src.db import mongo

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/', methods=['GET'])
def get_users():
    return {"message": "Hello, World!"}