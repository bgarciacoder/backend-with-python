from src.db import mongo
import datetime


def store_token(jti, user_id, device_id=None, user_agent=None, ip=None, expires_hours=24):
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=expires_hours)

    mongo.db.tokens.insert_one({
        "jti": jti,
        "user_id": user_id,
        "device_id": device_id,
        "user_agent": user_agent,
        "ip": ip,
        "created_at": datetime.datetime.utcnow(),
        "expires_at": expires_at,
        "revoked": False
    })


def is_token_revoked(jwt_payload):
    token = mongo.db.tokens.find_one({"jti": jwt_payload["jti"]})

    if token is None:
        return True

    # comprobar expiración manual
    if token["expires_at"] < datetime.datetime.utcnow():
        return True

    return token.get("revoked", False)


def revoke_token(jti):
    mongo.db.tokens.update_one(
        {"jti": jti},
        {"$set": {"revoked": True}}
    )