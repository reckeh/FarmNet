from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User
from datetime import timedelta

auth_bp = Blueprint('auth_bp', __name__)

# ------------------------
# REGISTER USER
# ------------------------
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check for required fields
    if not data.get('email'):
        return jsonify({'error': 'Email is required'}), 400
    if not data.get('password'):
        return jsonify({'error': 'Password is required'}), 400
    if not data.get('username'):
        return jsonify({'error': 'Username is required'}), 400
    if not data.get('role'):
        return jsonify({'error': 'Role is required'}), 400

    # Check if user with same email or username exists
    existing_user = User.query.filter(
        (User.email == data['email']) | (User.username == data['username'])
    ).first()
    if existing_user:
        return jsonify({'error': 'User with that email or username already exists'}), 409

    # Hash the password before saving it
    hashed_password = generate_password_hash(data['password'])

    # Create new user
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        role=data['role']  # Stored as Enum (convert from string in model constructor)
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# ------------------------
# LOGIN USER
# ------------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Check for required fields
    if not data.get('email'):
        return jsonify({'error': 'Email is required'}), 400
    if not data.get('password'):
        return jsonify({'error': 'Password is required'}), 400

    # Find user by email
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Create access token and include role in claims
    access_token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(days=1),
        additional_claims={"role": user.role.value}  # Use .value to serialize
    )

    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role.value  # Use .value for JSON serialization
        }
    }), 200

# ------------------------
# GET CURRENT USER
# ------------------------
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role.value  # Use .value
    })

# ------------------------
# PROTECTED ROUTE EXAMPLE
# ------------------------
@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Hello user {current_user}, you accessed a protected route'}), 200
