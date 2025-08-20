from flask import Blueprint, request, jsonify
from app import db
from app.models import Quiz, Question, Answer
from app.schemas import quiz_schema, quizzes_schema, question_schema, questions_schema, answer_schema, answers_schema

quizzes_bp = Blueprint('quizzes', __name__)

@quizzes_bp.route('/', methods=['GET'])
def get_quizzes():
    """Get all quizzes"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    active_only = request.args.get('active', 'true').lower() == 'true'
    
    query = Quiz.query
    if active_only:
        query = query.filter(Quiz.is_active == True)
    
    quizzes = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return jsonify({
        'quizzes': quizzes_schema.dump(quizzes.items),
        'total': quizzes.total,
        'pages': quizzes.pages,
        'current_page': page
    })

@quizzes_bp.route('/<quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """Get a specific quiz by ID"""
    quiz = Quiz.query.get_or_404(quiz_id)
    return jsonify(quiz_schema.dump(quiz))

@quizzes_bp.route('/<quiz_id>/questions', methods=['GET'])
def get_quiz_questions(quiz_id):
    """Get all questions for a specific quiz"""
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.question_order).all()
    return jsonify({
        'quiz_id': str(quiz_id),
        'questions': questions_schema.dump(questions)
    })

@quizzes_bp.route('/questions/<question_id>', methods=['GET'])
def get_question(question_id):
    """Get a specific question by ID"""
    question = Question.query.get_or_404(question_id)
    return jsonify(question_schema.dump(question))

@quizzes_bp.route('/questions/<question_id>/answers', methods=['GET'])
def get_question_answers(question_id):
    """Get all answers for a specific question"""
    question = Question.query.get_or_404(question_id)
    answers = Answer.query.filter_by(question_id=question_id).order_by(Answer.answer_order).all()
    return jsonify({
        'question_id': str(question_id),
        'answers': answers_schema.dump(answers)
    })

@quizzes_bp.route('/', methods=['POST'])
def create_quiz():
    """Create a new quiz"""
    data = request.get_json()
    
    quiz = Quiz(
        title=data['title'],
        slug=data['slug'],
        description=data.get('description'),
        is_active=data.get('is_active', True)
    )
    
    db.session.add(quiz)
    db.session.commit()
    
    return jsonify(quiz_schema.dump(quiz)), 201

@quizzes_bp.route('/<quiz_id>/questions', methods=['POST'])
def create_question():
    """Create a new question for a quiz"""
    data = request.get_json()
    
    question = Question(
        quiz_id=data['quiz_id'],
        question_text=data['question_text'],
        question_order=data.get('question_order', 0)
    )
    
    db.session.add(question)
    db.session.commit()
    
    return jsonify(question_schema.dump(question)), 201

@quizzes_bp.route('/questions/<question_id>/answers', methods=['POST'])
def create_answer():
    """Create a new answer for a question"""
    data = request.get_json()
    
    answer = Answer(
        question_id=data['question_id'],
        answer_text=data['answer_text'],
        is_correct=data.get('is_correct', False),
        answer_order=data.get('answer_order', 0)
    )
    
    db.session.add(answer)
    db.session.commit()
    
    return jsonify(answer_schema.dump(answer)), 201
