from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Feedback
from utils import role_required 
feedback_bp = Blueprint('feedback', __name__)

# SUBMIT FEEDBACK
@feedback_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_feedback():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get('message'):
        return jsonify({'message': 'Feedback message is required.'}), 400

    feedback = Feedback(
        user_id=user_id,
        message=data['message'],
        status='Pending'
    )

    try:
        feedback.save()
        return jsonify({'message': 'Feedback submitted successfully.'}), 201
    except Exception as e:
        return jsonify({'message': f'Error submitting feedback: {str(e)}'}), 500


# GET ALL FEEDBACK (FOR ADMIN )
@feedback_bp.route('/all', methods=['GET'])
@jwt_required()
@role_required('admin')  # Only admin can access this endpoint
def get_all_feedback():
    user_id = get_jwt_identity()

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    feedbacks = Feedback.query.paginate(page, per_page, False)

    if not feedbacks.items:
        return jsonify({'message': 'No feedback found.'}), 404

    feedback_list = []
    for feedback in feedbacks.items:
        feedback_list.append({
            'user_id': feedback.user_id,
            'message': feedback.message,
            'status': feedback.status,
            'date': feedback.date
        })

    return jsonify({
        'feedback': feedback_list,
        'total': feedbacks.total,
        'page': page,
        'per_page': per_page
    }), 200


# RESOLVE FEEDBACK (FOR ADMIN)
@feedback_bp.route('/resolve/<int:feedback_id>', methods=['PUT'])
@jwt_required()
@role_required('support')  
def resolve_feedback(feedback_id):
    user_id = get_jwt_identity()

    feedback = Feedback.query.filter_by(id=feedback_id).first()

    if not feedback:
        return jsonify({'message': 'Feedback not found.'}), 404

    feedback.status = 'Resolved'

    try:
        feedback.save()
        return jsonify({'message': 'Feedback marked as resolved.'}), 200
    except Exception as e:
        return jsonify({'message': f'Error resolving feedback: {str(e)}'}), 500
