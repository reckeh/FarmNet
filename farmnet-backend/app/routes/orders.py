from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Order, OrderItem, Product, Delivery, User

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_farmer_orders():
    farmer_id = get_jwt_identity()

    # Get all OrderItems that belong to the current farmer's products
    items = OrderItem.query.join(Product).filter(Product.farmer_id == farmer_id).all()

    # Extract unique order IDs
    unique_orders = {}
    for item in items:
        order = item.order
        if order.id not in unique_orders:
            unique_orders[order.id] = order

    # Compile data
    orders_data = []
    for order in unique_orders.values():
        delivery = order.delivery
        orders_data.append({
            "order_id": order.id,
            "status": order.status.value,
            "total_price": order.total_price,
            "order_date": order.order_date.isoformat(),
            "items": [
                {
                    "product_id": i.product_id,
                    "product_name": i.product.name,
                    "product_image": i.product.image_url,
                    "quantity": i.quantity,
                    "unit_price": i.product.price
                }
                for i in order.items if i.product.farmer_id == farmer_id
            ],
            "delivery": delivery.to_dict() if delivery else None
        })

    return jsonify(orders_data), 200
