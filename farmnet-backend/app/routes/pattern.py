from flask import Blueprint, jsonify
from app.models import db, User
from sqlalchemy import text


pattern_bp = Blueprint('pattern', __name__)

@pattern_bp.route('/pattern', methods=['GET'])
def get_usage():
    total_users = User.query.count()

    total_logins = 0  
    active_sessions = 0

    result = db.session.execute(text('SELECT id, username, action, date FROM logs ORDER BY date DESC'))
    logs = [
        {
            "id": row.id,
            "user": row.username,
            "action": row.action,
            "date": row.date.strftime('%Y-%m-%d %H:%M')
        }
        for row in result
    ]

    usage_data = {
        "totalUsers": total_users,
        "totalLogins": total_logins,
        "activeSessions": active_sessions,
        "logs": logs
    }

    return jsonify(usage_data)
