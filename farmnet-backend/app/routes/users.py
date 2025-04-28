from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User
from werkzeug.security import generate_password_hash
from app.models import UserRole

import re

users_bp = Blueprint('users', __name__)

# Helper function to validate email format
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

# GET user profile
@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role.value  # Convert Enum to string
    })

# UPDATE user profile
@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Validate username (for example, no empty string)
    if "username" in data and not data["username"]:
        return jsonify({"error": "Username cannot be empty"}), 400

    # Validate email format
    if "email" in data and not is_valid_email(data["email"]):
        return jsonify({"error": "Invalid email format"}), 400

    # Update the username and email if provided
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)

    # Optional: Add password update
    if data.get("password"):
        user.password = generate_password_hash(data["password"])

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"}), 200

@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_users():
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != UserRole.ADMIN:
        return jsonify({"error": "Unauthorized"}), 403

    users = User.query.all()
    return jsonify([{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role.value
    } for user in users]), 200


# Admin: Create a new user
@users_bp.route('/', methods=['POST'])
@jwt_required()
def create_user():
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != UserRole.ADMIN:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    if not is_valid_email(data.get("email", "")):
        return jsonify({"error": "Invalid email format"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 409

    new_user = User(
        username=data["username"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        role=UserRole[data.get("role", "FARMER").upper()]
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created"}), 201


# Admin: Update user by ID
@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def admin_update_user(user_id):
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != UserRole.ADMIN:
        return jsonify({"error": "Unauthorized"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if "email" in data and not is_valid_email(data["email"]):
        return jsonify({"error": "Invalid email format"}), 400

    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    if data.get("password"):
        user.password = generate_password_hash(data["password"])
    if data.get("role"):
        user.role = UserRole[data["role"].upper()]

    db.session.commit()
    return jsonify({"message": "User updated"}), 200


# Admin: Delete user
@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != UserRole.ADMIN:
        return jsonify({"error": "Unauthorized"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200