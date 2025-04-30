from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, Order, OrderItem, Product, Transaction, Delivery, OrderStatus, TransactionType, UserRole

from app.models import db, Cart

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')


# Handle Preflight CORS Request
@cart_bp.route('', methods=['OPTIONS'])
def handle_options():
    return '', 200


# Get Cart Items for Logged-in User
@cart_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    
    # Join Cart with Product table to get full product details
    cart_items = db.session.query(Cart, Product).join(Product, Cart.product_id == Product.id).filter(Cart.user_id == user_id).all()

    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 404

    # Process cart data to include product details
    cart_data = []
    total_price = 0
    
    for cart_item, product in cart_items:
        item_data = {
            "id": cart_item.id,
            "product_id": product.id,
            "product_name": product.name,
            "product_image": product.image_url,  # Or adjust the image field name if different
            "price": product.price,
            "quantity": cart_item.quantity,
            "user_id": cart_item.user_id
        }
        # Calculate total price for each cart item
        total_price += product.price * cart_item.quantity
        cart_data.append(item_data)

    return jsonify({"cart": cart_data, "total_price": total_price}), 200


# Add Item to Cart
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


# Place Order from Cart
@jwt_required()
@cart_bp.route('/order', methods=['POST'])
def place_order():
    try:
        # Get request data
        data = request.get_json()
        
        # Ensure buyer_id exists in the request
        buyer_id = data.get('buyer_id')
        if not buyer_id:
            return jsonify({"error": "buyer_id is required"}), 400

        items = data.get('items', [])
        if not items:
            return jsonify({"error": "Items are required"}), 400

        delivery_address = data.get('delivery_address')
        delivery_method = data.get('delivery_method')
        if not delivery_address or not delivery_method:
            return jsonify({"error": "Delivery address and method are required"}), 400

        # Create the order
        order = Order(buyer_id=buyer_id, total_price=0.0)
        db.session.add(order)
        db.session.commit()  # Commit to get the order ID

        total_price = 0
        for item in items:
            product = Product.query.get(item['product_id'])
            if product and product.quantity >= item['quantity']:  # Check if there's enough stock
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=item['quantity'],
                    price=product.price
                )
                db.session.add(order_item)
                total_price += product.price * item['quantity']
            else:
                return jsonify({"error": "Not enough stock for product " + product.name}), 400

        # Update total price of the order
        order.total_price = total_price
        db.session.commit()

        # Create a transaction for the order payment
        transaction = Transaction(
            user_id=buyer_id,
            amount=total_price,
            transaction_type=TransactionType.PURCHASE,
            description=f"Payment for Order #{order.id}"
        )
        db.session.add(transaction)
        db.session.commit()

        # Create delivery record
        delivery = Delivery(
            order_id=order.id,
            courier_id=None,  
            address=delivery_address,
            method=delivery_method,
            status='Pending'
        )
        db.session.add(delivery)
        db.session.commit()

        # Update order status
        order.status = OrderStatus.PROCESSING
        db.session.commit()

        return jsonify({
            'order_id': order.id,
            'total_price': order.total_price,
            'status': order.status.value,
            'delivery_address': delivery_address
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get User Orders with Delivery Info
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
