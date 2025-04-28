from flask import Blueprint, jsonify
from app.models import db, User, Transaction

reports_bp = Blueprint('reports', __name__)

# Report for total users
@reports_bp.route('/reports/total_users', methods=['GET'])
def get_total_users():
    total_users = User.query.count()
    return jsonify({"totalUsers": total_users})

# Report for total transactions
@reports_bp.route('/reports/total_transactions', methods=['GET'])
def get_total_transactions():
    total_transactions = Transaction.query.count()  # Assuming a Transaction model exists
    return jsonify({"totalTransactions": total_transactions})

# Example of generating a custom report (total revenue or total sales)
@reports_bp.route('/reports/total_revenue', methods=['GET'])
def get_total_revenue():
    total_revenue = db.session.query(db.func.sum(Transaction.amount)).scalar()  # Example logic
    return jsonify({"totalRevenue": total_revenue})
