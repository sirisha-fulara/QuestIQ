import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.quiz import Quiz
from models.question import Question, Option
from services.ai_service import generate_quiz_questions
from models.attempt import Attempt

quiz_bp = Blueprint("quiz", __name__, url_prefix="/quiz")


def normalize_question(q):
    if not isinstance(q, dict):
        raise ValueError(f"Expected dict, got {type(q)}")

    question_text = (
        q.get("question")
        or q.get("Question")
        or q.get("question_text")
        or q.get("prompt")
    )

    options = q.get("options") or q.get("choices")

    correct_answer = (
        q.get("correct_answer")
        or q.get("answer")
        or q.get("correct")
    )

    if not question_text or not isinstance(options, dict) or not correct_answer:
        raise ValueError(f"Invalid AI question format: {q}")

    return question_text, options, correct_answer.upper()


@quiz_bp.route("/generate", methods=["POST"])
@jwt_required()
def generate_quiz():
    data = request.json

    title = data.get("title")
    topic = data.get("topic")
    difficulty = data.get("difficulty")

    user_id = int(get_jwt_identity())

    if not title or not topic:
        return jsonify({"message": "Title and topic missing"}), 400

    #Create quiz
    quiz = Quiz(
        title=title,
        difficulty=difficulty,
        created_by=user_id
    )
    db.session.add(quiz)
    db.session.flush()

    #Generate questions via AI
    questions_data = generate_quiz_questions(topic, difficulty)

    if isinstance(questions_data, str):
        questions_data = json.loads(questions_data)

    if isinstance(questions_data, dict):
        questions_data = [questions_data]

    #Save questions and options
    for q in questions_data:
        question_text, options_dict, correct_answer = normalize_question(q)

        question = Question(
            quiz_id=quiz.id,
            question_text=question_text,
            correct_option=correct_answer
        )
        db.session.add(question)
        db.session.flush()

        for key, value in options_dict.items():
            option = Option(
                question_id=question.id,
                option_key=key,
                option_text=value
            )
            db.session.add(option)

    db.session.commit()

    return jsonify({
        "message": "Quiz generated successfully",
        "quiz_id": quiz.id
    }), 201


@quiz_bp.route('/<int:quiz_id>', methods=['GET', 'OPTIONS'])
@jwt_required(optional=True)
def get_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    questions = []

    for q in quiz.questions:
        options = {
            opt.option_key: opt.option_text
            for opt in q.options
        }

        questions.append({
            "id": q.id,
            "question_text": q.question_text,
            "options": options,
            "correct_option": q.correct_option
        })

    return jsonify(questions), 200

@quiz_bp.route('/<int:quiz_id>/submit', methods=['POST'])
@jwt_required()
def submit_quiz(quiz_id):
    user_id= int(get_jwt_identity())
    data= request.json
    
    score= data.get("score")
    total= data.get("total")
    
    if score is None or total is None:
        return jsonify({"message": "invalid submission"}), 400
    
    attempt= Attempt(
        user_id= user_id,
        quiz_id= quiz_id,
        score= score,
        total_questions= total
    )
    db.session.add(attempt)
    db.session.commit()
    
    return jsonify({"message": "Attempt saved successfully"}), 201

@quiz_bp.route('/attempts', methods=['GET'])
@jwt_required()
def get_attempts():
    user_id= int(get_jwt_identity())
    
    attempts= db.session.query(Attempt, Quiz).join(Quiz, Attempt.quiz_id==Quiz.id).filter(Attempt.user_id==user_id).order_by(Attempt.created_at.desc()).all()
    
    return jsonify([
        {
            'quiz_id': quiz.id,
            'quiz_title': quiz.title,
            'difficulty': quiz.difficulty,
            'score': attempt.score,
            'total': attempt.total_questions,
            'accuracy': round((attempt.score/attempt.total_questions) *100, 2),
            'date': attempt.created_at.strftime("%d %b %Y, %H:%M")
        }
        for attempt, quiz in attempts
    ])
    
@quiz_bp.route("/analytics", methods=['GET'])
@jwt_required()
def get_analytics():
    user_id= int(get_jwt_identity())
    attempts= Attempt.query.filter_by(user_id=user_id).all()
    
    if not attempts:
        return jsonify({
            'total_attempts': 0,
            'average_score': 0,
            'average_accuracy': 0
        })
        
    total_attempts= len(attempts)
    total_score= sum(a.score for a in attempts)
    total_questions= sum(a.total_questions for a in attempts)
    
    return jsonify({
        "total_attempts": total_attempts,
        "average_score": round(total_score / total_attempts, 2),
        "average_accuracy": round((total_score / total_questions) * 100, 2)
    }) 
    
@quiz_bp.route("/topic-analytics", methods=["GET"])
@jwt_required()
def topic_analytics():
    user_id = int(get_jwt_identity())

    rows = (
        db.session.query(Attempt, Quiz)
        .join(Quiz, Attempt.quiz_id == Quiz.id)
        .filter(Attempt.user_id == user_id)
        .all()
    )

    topic_stats = {}

    for attempt, quiz in rows:
        topic = quiz.title 

        if topic not in topic_stats:
            topic_stats[topic] = {
                "score": 0,
                "total": 0
            }

        topic_stats[topic]["score"] += attempt.score
        topic_stats[topic]["total"] += attempt.total_questions

    return jsonify([
        {
            "topic": topic,
            "accuracy": round((data["score"] / data["total"]) * 100, 2)
        }
        for topic, data in topic_stats.items()
    ])
