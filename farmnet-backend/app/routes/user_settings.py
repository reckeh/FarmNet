from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
import re

user_settings_bp = Blueprint('user_settings', __name__)

# --------------------------
# UPDATE USER PROFILE
# --------------------------
@user_settings_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found.'}), 404

    data = request.get_json()

    # Validate email format
    email = data.get('email', user.email)
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email format.'}), 400

    # Update the user profile fields
    user.name = data.get('name', user.name)
    user.email = email

    db.session.commit()

    return jsonify({
        'message': 'Profile updated successfully',
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
    }), 200


# --------------------------
# CHANGE USER PASSWORD
# --------------------------
@user_settings_bp.route('/password', methods=['PUT'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found.'}), 404

    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    # Validate presence of passwords
    if not old_password or not new_password:
        return jsonify({'error': 'Old and new passwords are required.'}), 400

    # Ensure new password is long enough
    if len(new_password) < 8:
        return jsonify({'error': 'New password must be at least 8 characters long.'}), 400

    # Verify old password
    if not check_password_hash(user.password, old_password):
        return jsonify({'error': 'Old password is incorrect.'}), 401

    # Hash and update the new password
    user.password = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({
        'message': 'Password updated successfully'
    }), 200


# --------------------------
# UPDATE USER PREFERENCES
# --------------------------
@user_settings_bp.route('/preferences', methods=['PUT'])
@jwt_required()
def update_preferences():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found.'}), 404

    data = request.get_json()

    # Assuming preferences are stored as JSON (you can add validation here if needed)
    user.preferences = data.get('preferences', user.preferences)

    db.session.commit()

    return jsonify({
        'message': 'Preferences updated successfully',
        'preferences': user.preferences
    }), 200


# Helper function to validate email format
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)
