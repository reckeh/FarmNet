from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Cart, Product, Order, OrderItem, Delivery

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')


# ------------------------------
# Handle Preflight CORS Request
# ------------------------------
@cart_bp.route('', methods=['OPTIONS'])
def handle_options():
    return '', 200


# ------------------------------
# Get Cart Items for Logged-in User
# ------------------------------
@cart_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 404

    cart_data = [item.to_dict() for item in cart_items]
    return jsonify({"cart": cart_data}), 200


# ------------------------------
# Add Item to Cart
# ------------------------------
@cart_bp.route('', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()

    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not product_id or quantity is None:
        return jsonify({"message": "Product ID and quantity are required"}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    existing_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing_item:
        existing_item.quantity += quantity
    else:
        new_cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(new_cart_item)

    db.session.commit()
    return jsonify({"message": "Item added to cart successfully"}), 201


# ------------------------------
# Place Order from Cart
# ------------------------------
@cart_bp.route('/order', methods=['POST'])
@jwt_required()
def place_order():
    user_id = get_jwt_identity()
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 400

    # Validate delivery info
    delivery_data = request.get_json().get('delivery_info', {})
    delivery_address = delivery_data.get('address')
    delivery_method = delivery_data.get('method')
    delivery_status = delivery_data.get('status', 'Pending')

    if not delivery_address or not delivery_method:
        return jsonify({"message": "Delivery address and method are required"}), 400

    # Create order
    new_order = Order(buyer_id=user_id, total_price=0)  # Placeholder
    db.session.add(new_order)
    db.session.flush()

    total_price = 0
    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        if not product:
            continue
        item_total = product.price * cart_item.quantity
        total_price += item_total

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=cart_item.quantity,
            price=product.price
        )
        db.session.add(order_item)

    new_order.total_price = total_price
    db.session.commit()

    # Clear cart
    Cart.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    # Add delivery info
    new_delivery = Delivery(
        order_id=new_order.id,
        address=delivery_address,
        method=delivery_method,
        status=delivery_status
    )
    db.session.add(new_delivery)
    db.session.commit()

    return jsonify({
        "message": "Order created successfully",
        "order_id": new_order.id,
        "total_price": total_price,
        "delivery_info": delivery_data
    }), 201


# ------------------------------
# Get User Orders with Delivery Info
# ------------------------------
@cart_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(buyer_id=user_id).all()

    if not orders:
        return jsonify({"message": "No orders found"}), 404

    orders_data = []
    for order in orders:
        delivery_info = Delivery.query.filter_by(order_id=order.id).first()
        order_data = order.to_dict()
        order_data["delivery_info"] = delivery_info.to_dict() if delivery_info else None
        orders_data.append(order_data)

    return jsonify({"orders": orders_data}), 200
