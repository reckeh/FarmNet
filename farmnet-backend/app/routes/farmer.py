import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.models import db, Product, MarketPrice

farmer_bp = Blueprint('farmer', __name__)

# Helper function to save image and return URL
def save_image(image_file):
    # Generate a unique filename to avoid overwriting
    filename = secure_filename(image_file.filename)
    # You can also append a timestamp or UUID to make filenames unique
    filename = f"{int(time.time())}_{filename}"
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)
    image_file.save(filepath)
    return f"/static/uploads/{filename}"

# Helper function to validate image file type
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create a new product (POST /api/farmer/products)
@farmer_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    user_id = get_jwt_identity()

    # Handle FormData
    name = request.form.get('name')
    description = request.form.get('description', '')
    price = request.form.get('price', type=float)
    quantity = request.form.get('quantity', type=int)
    image = request.files.get('image')

    # Basic validation for required fields
    if not name or price is None or quantity is None:
        return jsonify({"message": "Name, price, and quantity are required."}), 400

    if price <= 0 or quantity <= 0:
        return jsonify({"message": "Price and quantity must be positive numbers."}), 400

    # Validate and save image if provided
    image_url = None
    if image:
        if not allowed_file(image.filename):
            return jsonify({"message": "Invalid image format. Only PNG, JPG, and JPEG are allowed."}), 400
        image_url = save_image(image)

    # Create and store product
    product = Product(
        name=name,
        description=description,
        price=price,
        quantity=quantity,
        image_url=image_url,
        farmer_id=user_id
    )

    try:
        db.session.add(product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error saving product: {str(e)}"}), 500

    return jsonify({
        "message": "Product created successfully",
        "product_id": product.id,
        "image_url": image_url
    }), 201

# Get all products for the current farmer (GET /api/farmer/products)
@farmer_bp.route('/products', methods=['GET'])
@jwt_required()
def get_my_products():
    user_id = get_jwt_identity()
    products = Product.query.filter_by(farmer_id=user_id).all()

    if not products:
        return jsonify({"message": "No products found for this farmer."}), 404

    products_data = [{
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "price": p.price,
        "quantity": p.quantity,
        "image_url": p.image_url
    } for p in products]

    return jsonify(products_data), 200

# Get market prices (GET /api/farmer/market-prices?county=...)
@farmer_bp.route('/market-prices', methods=['GET'])
def get_market_prices():
    county = request.args.get('county')

    if county:
        prices = MarketPrice.query.filter_by(county=county).all()
    else:
        prices = MarketPrice.query.all()

    if not prices:
        return jsonify({"message": "No market prices found."}), 404

    prices_data = [{"product": price.product_name, "price": price.price} for price in prices]
    return jsonify(prices_data), 200
