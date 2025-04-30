from flask import Blueprint, jsonify
from app.models import db, User, Transaction

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports/total_users', methods=['GET'])
def get_total_users():
    total_users = User.query.count()
    return jsonify({"totalUsers": total_users})

@reports_bp.route('/reports/total_transactions', methods=['GET'])
def get_total_transactions():
    total_transactions = Transaction.query.count()  
    return jsonify({"totalTransactions": total_transactions})

@reports_bp.route('/reports/total_revenue', methods=['GET'])
def get_total_revenue():
    total_revenue = db.session.query(db.func.sum(Transaction.amount)).scalar()  
    return jsonify({"totalRevenue": total_revenue})
