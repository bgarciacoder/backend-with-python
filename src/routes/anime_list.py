from flask import Blueprint, jsonify, request
from src.db import mongo
from src.middleware.api_key_required import api_key_required
from src.middleware.jwt_required import jwt_required

anilist_bp = Blueprint('anilist', __name__, url_prefix='/anilist')

# Get the anime list for a specific user
@anilist_bp.route('/<user_id>', methods=['GET'])
@api_key_required
@jwt_required
def get_anime_list_by_user(user_id):
    # Example: Fetch the anime list for a specific user
    anime_list = mongo.db.usersAnimeList.find({"user_id": user_id})
    return jsonify([anime for anime in anime_list])


# Add a new anime item to the user's list
@anilist_bp.route('/add', methods=['POST'])
@api_key_required
@jwt_required
def add_anime_item():
    data = request.get_json()
    if not data:
        return jsonify({
            "error": "No data provided",
            "status": "failed",
            "code": 400
            }), 400

    mongo.db.usersAnimeList.insert_one(data)

    # Example: Add the item to the database
    # mongo.db.anime_list.insert_one(data)

    return {
            "message": "Item added successfully", 
            "status": "success",
            "code": 201
            }, 201