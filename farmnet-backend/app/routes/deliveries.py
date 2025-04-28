from flask import Blueprint, jsonify, request
from app.models import db, Delivery, Order
from datetime import datetime

deliveries_bp = Blueprint('deliveries', __name__, url_prefix='/api/deliveries')

# Get all deliveries
@deliveries_bp.route('/', methods=['GET'])
def get_deliveries():
    deliveries = Delivery.query.all()
    results = []
    for delivery in deliveries:
        results.append({
            'delivery_id': delivery.id,
            'order_id': delivery.order_id,
            'driver_id': delivery.driver_id,
            'pickup_location': delivery.pickup_location,
            'dropoff_location': delivery.dropoff_location,
            'status': delivery.status.value if delivery.status else None,
            'scheduled_time': delivery.scheduled_time.isoformat() if delivery.scheduled_time else None
        })
    return jsonify(results), 200

# Create a new delivery
@deliveries_bp.route('/', methods=['POST'])
def create_delivery():
    data = request.get_json()
    order_id = data.get('order_id')
    driver_id = data.get('driver_id')
    pickup_location = data.get('pickup_location')
    dropoff_location = data.get('dropoff_location')
    scheduled_time = datetime.strptime(data.get('scheduled_time'), "%Y-%m-%dT%H:%M:%S")

    new_delivery = Delivery(
        order_id=order_id,
        driver_id=driver_id,
        pickup_location=pickup_location,
        dropoff_location=dropoff_location,
        scheduled_time=scheduled_time,
        status="PENDING"
    )
    db.session.add(new_delivery)
    db.session.commit()

    return jsonify({'message': 'Delivery created successfully'}), 201
