from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.models import db, Product
import os

# Initialize blueprint
products_bp = Blueprint('products', __name__)

# Folder for storing uploaded images
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create a new product
@products_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    image = request.files.get('image')
    
    # Debugging prints (you can comment these later)
    print("Image Object:", image)
    print("Image Filename:", image.filename if image else "No image received")

    data = request.form
    user_id = get_jwt_identity()

    if not data.get("name") or not data.get("price") or not data.get("quantity"):
        return jsonify({"message": "Name, price, and quantity are required."}), 400

    image_url = None

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image.save(filepath)
        image_url = f"/uploads/{filename}"

    new_product = Product(
        farmer_id=user_id,
        name=data["name"],
        description=data.get("description"),
        price=data["price"],
        quantity=data["quantity"],
        unit=data.get("unit", "kg"),
        available=True,
        image_url=image_url
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product created successfully", "image_url": image_url}), 201

# Get all available products
@products_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.filter_by(available=True).all()
    result = [{
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "price": p.price,
        "quantity": p.quantity,
        "unit": p.unit,
        "farmer_id": p.farmer_id,
        "image_url": p.image_url
    } for p in products]

    return jsonify(result), 200

# Get all products for the logged-in farmer
@products_bp.route('/products/my', methods=['GET'])
@jwt_required()
def get_my_products():
    user_id = get_jwt_identity()
    products = Product.query.filter_by(farmer_id=user_id).all()
    result = [{
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "price": p.price,
        "quantity": p.quantity,
        "unit": p.unit,
        "available": p.available,
        "image_url": p.image_url
    } for p in products]

    return jsonify(result), 200

# Update a product
@products_bp.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    user_id = get_jwt_identity()
    data = request.form
    image = request.files.get('image')

    product = Product.query.filter_by(id=product_id, farmer_id=user_id).first()
    if not product:
        return jsonify({"error": "Product not found or unauthorized"}), 404

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image.save(filepath)
        product.image_url = f"/uploads/{filename}"

    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.quantity = data.get("quantity", product.quantity)
    product.unit = data.get("unit", product.unit)

    # Handle boolean properly
    available = data.get("available")
    if available is not None:
        product.available = available.lower() == "true"

    db.session.commit()

    return jsonify({"message": "Product updated successfully", "image_url": product.image_url}), 200

# Delete a product
@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    user_id = get_jwt_identity()
    product = Product.query.filter_by(id=product_id, farmer_id=user_id).first()

    if not product:
        return jsonify({"error": "Product not found or unauthorized"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted successfully"}), 200
