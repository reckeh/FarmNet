from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, MarketPrice, User
from datetime import datetime

market_prices_bp = Blueprint('market_prices', __name__)

@market_prices_bp.route('/prices', methods=['POST'])
@jwt_required()
def add_market_price():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or user.role != 'government':
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    required_fields = ['commodity', 'county', 'retail_price']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        price = MarketPrice(
            commodity=data['commodity'],
            county=data['county'],
            retail_price=data['retail_price'],
            wholesale_price=data.get('wholesale_priceu',),
            date=datetime.utcnow()
        )
        db.session.add(price)
        db.session.commit()

        return jsonify({
            "message": "Market price added successfully",
            "data": {
                "id": price.id,
                "commodity": price.commodity,
                "county": price.county,
                "retail_price": price.retail_price,
                "wholesale_price": price.wholesale_price,
                "date": price.date.strftime('%Y-%m-%d')
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to add market price: {str(e)}"}), 500


@market_prices_bp.route('/prices', methods=['GET'])
def get_market_prices():
    commodity = request.args.get('commodity')
    county = request.args.get('county')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)  # cap per_page to 50

    query = MarketPrice.query

    if commodity:
        query = query.filter(MarketPrice.product_name.ilike(f'%{commodity}%'))
    if county:
        query = query.filter(MarketPrice.county.ilike(f'%{county}%'))
    if start_date:
        try:
            query = query.filter(MarketPrice.date >= datetime.strptime(start_date, '%Y-%m-%d'))
        except ValueError:
            return jsonify({'error': 'Invalid start_date format. Use YYYY-MM-DD'}), 400
    if end_date:
        try:
            query = query.filter(MarketPrice.date <= datetime.strptime(end_date, '%Y-%m-%d'))
        except ValueError:
            return jsonify({'error': 'Invalid end_date format. Use YYYY-MM-DD'}), 400

    prices = db.paginate(
        query.order_by(MarketPrice.date.desc()),
        page=page,
        per_page=per_page,
        error_out=False
    )

    results = [{
        "id": p.id,
        "commodity": p.commodity,
        "county": p.county,
        "retail_price": p.retail_price,
        "wholesale_price": p.wholesale_price,
        "date": p.date.strftime('%Y-%m-%d')
    } for p in prices.items]

    return jsonify({
        'data': results,
        'pagination': {
            'page': prices.page,
            'per_page': prices.per_page,
            'total': prices.total,
            'pages': prices.pages
        }
    }), 200
