# auth_service.py
from flask import Blueprint, request, jsonify
import bcrypt
import uuid
from database import insert_user, get_user
from typing import Dict

auth_bp = Blueprint('auth', __name__)
# simple in-memory session store: token -> username
sessions: Dict[str, str] = {}

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400
    if get_user(username):
        return jsonify({"error": "user exists"}), 400
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    insert_user(username, pw_hash)
    return jsonify({"status": "registered"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")
    row = get_user(username)
    if not row:
        return jsonify({"error": "invalid credentials"}), 401
    _, _, pw_hash = row
    if not bcrypt.checkpw(password.encode(), pw_hash.encode()):
        return jsonify({"error": "invalid credentials"}), 401
    token = str(uuid.uuid4())
    sessions[token] = username
    return jsonify({"token": token})

@auth_bp.route("/validate-session", methods=["POST"])
def validate_session():
    data = request.json or {}
    token = data.get("token")
    if token in sessions:
        return jsonify({"valid": True, "username": sessions[token]})
    return jsonify({"valid": False}), 401

# helper for other modules to validate
def validate_token_from_header(headers):
    auth = headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth.split(" ")[1]
        return token if token in sessions else None
    return None
