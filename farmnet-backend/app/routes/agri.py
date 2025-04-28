# app/routes/agri.py
from flask import Blueprint, request, jsonify
from app.models import db, Article, Question, Answer  # Assuming you have models for Article, Question, and Answer
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create Blueprint for articles and Q&A
agri_bp = Blueprint('agri', __name__)

# Route for fetching all articles
@agri_bp.route('/articles', methods=['GET'])
def get_articles():
    articles = Article.query.all()
    result = [{
        "id": article.id,
        "title": article.title,
        "content": article.content,
        "created_at": article.created_at
    } for article in articles]

    return jsonify(result), 200


# Route for adding a new article (requires authentication)
@agri_bp.route('/articles', methods=['POST'])
@jwt_required()
def create_article():
    user = get_jwt_identity()
    data = request.get_json()

    if not data.get('title') or not data.get('content'):
        return jsonify({"message": "Title and content are required."}), 400

    new_article = Article(
        title=data['title'],
        content=data['content'],
        author_id=user["id"]
    )

    db.session.add(new_article)
    db.session.commit()

    return jsonify({"message": "Article created successfully"}), 201


# Route for fetching all questions related to an article
@agri_bp.route('/articles/<int:article_id>/questions', methods=['GET'])
def get_questions(article_id):
    questions = Question.query.filter_by(article_id=article_id).all()
    result = [{
        "id": question.id,
        "question": question.question_text,
        "asked_by": question.asked_by,
        "created_at": question.created_at
    } for question in questions]

    return jsonify(result), 200


# Route for adding a new question (requires authentication)
@agri_bp.route('/articles/<int:article_id>/questions', methods=['POST'])
@jwt_required()
def create_question(article_id):
    user = get_jwt_identity()
    data = request.get_json()

    if not data.get('question_text'):
        return jsonify({"message": "Question text is required."}), 400

    new_question = Question(
        article_id=article_id,
        question_text=data['question_text'],
        asked_by=user["id"]
    )

    db.session.add(new_question)
    db.session.commit()

    return jsonify({"message": "Question added successfully"}), 201


# Route for answering a question (requires authentication)
@agri_bp.route('/questions/<int:question_id>/answers', methods=['POST'])
@jwt_required()
def answer_question(question_id):
    user = get_jwt_identity()
    data = request.get_json()

    if not data.get('answer_text'):
        return jsonify({"message": "Answer text is required."}), 400

    question = Question.query.get_or_404(question_id)

    new_answer = Answer(
        question_id=question_id,
        answer_text=data['answer_text'],
        answered_by=user["id"]
    )

    db.session.add(new_answer)
    db.session.commit()

    return jsonify({"message": "Answer added successfully"}), 201


# Route for fetching answers to a specific question
@agri_bp.route('/questions/<int:question_id>/answers', methods=['GET'])
def get_answers(question_id):
    answers = Answer.query.filter_by(question_id=question_id).all()
    result = [{
        "id": answer.id,
        "answer_text": answer.answer_text,
        "answered_by": answer.answered_by,
        "created_at": answer.created_at
    } for answer in answers]

    return jsonify(result), 200
