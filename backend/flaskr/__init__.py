import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  cors = CORS(app, resources={r"*": {"origins": "*"}})
    
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response


  def paginate_questions(questions, page):
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    current_questions = questions[start:end]
    return current_questions

  @app.route('/categories')
  def get_categories():

    try:
      categories = Category.query.all()
      return jsonify({
        'success':True,
        'status':200,
        'message':'successfully fetched all categories',
        'categories':[c.format() for c in categories]
      })
    except:
      abort(422)

  @app.route('/questions')
  def get_questions():
    page = request.args.get('page', 1, type=int)
    error = None

    try:
      questions = Question.query.all()
      categories = Category.query.all()
      formatted_questions = [q.format() for q in questions]

      results = paginate_questions(formatted_questions, page)

      if len(results) == 0:
        error = 404
        abort(404)

      return jsonify({
        'success':True,
        'status':200,
        'message':'successfully fetched questions',
        'questions': results,
        'total_questions': len(formatted_questions),
        'categories': [c.format() for c in categories]
      })
    except:
      if error == 404:
        abort(404)
      else:
        abort(422)

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

    error = None

    try:
      question = Question.query.filter_by(id=question_id).one_or_none()

      if question is None:
        error = 404
        abort(404)
      else:
        question.delete()

        return jsonify({
          'success':True,
          'status':200,
          'message':'successfully deleted question'
        })
    except:
      if error == 404:
        abort(404)
      else:
        abort(422)

  @app.route('/questions', methods=['POST'])
  def post_question():
    body = request.get_json()

    fresh_question = body.get('question')
    new_answer = body.get('answer')
    new_category = body.get('category')
    new_difficulty = body.get('difficulty')

    if fresh_question is None  or new_answer is None \
      or new_category is None or new_difficulty is None: 
        abort(400)

    new_question = Question(
      question=fresh_question,
      answer=new_answer,
      category=new_category,
      difficulty=new_difficulty
    )

    try:
      new_question.insert()

      return jsonify({
        'success':True,
        'status':201,
        'message':'successfully created a question',
        'created_question': new_question.id
      }), 201
    except:
      abort(422)

  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    body = request.get_json()
    search_term = body.get('searchTerm')

    try:
      found_questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

      return jsonify({
        'success':True,
        'status':200,
        'message':'successfully found questions',
        'questions':[q.format() for q in found_questions]
      })
    except:
      abort(422)

  @app.route('/categories/<int:category_id>/questions')
  def get_category_questions(category_id):
    page = request.args.get('page', 1)

    try:
      questions = Question.query.filter_by(category=category_id).all()
      formatted_questions = [q.format() for q in questions]

      results = paginate_questions(formatted_questions, page)

      return jsonify({
        'success':True,
        'status':200,
        'message':'successfully returned questions by category',
        'questions': results
      })
    except:
      abort(422)

  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    body = request.get_json()
    previous_questions = body.get('previous_questions', [])
    category = body.get('quiz_category')

    try:
      questions = Question.query.filter_by(category=category['id']).all()

      formatted_questions = [q.format() for q in questions]

      available_questions = []

      for q in formatted_questions:
        
        if q['id'] not in previous_questions:
          available_questions.append(q)

      next_question = None

      if len(available_questions) > 0:
        random_index = random.randint(0, len(available_questions) - 1)
        next_question = available_questions[random_index]

      return jsonify({
        'success':True,
        'status':200,
        'message':'successfully returned questions by category',
        'question': next_question
      })
    except:
      abort(422)

  @app.errorhandler(400)
  def bad_request(e):
    return jsonify({
      'success':False,
      'status':400,
      'message':'bad request'
    }), 400

  @app.errorhandler(404)
  def not_found(e):
    return jsonify({
      'success':False,
      'status':404,
      'message':'resource not found'
    }), 404

  @app.errorhandler(422)
  def unprocessible(e):
    print(e)
    return jsonify({
      'success':False,
      'status':422,
      'message':'unprocessible request'
    }), 422

  @app.errorhandler(405)
  def method_not_allowed(e):
    return jsonify({
      'success':False,
      'status':405,
      'message':'method not allowed'
    }), 405
  
  return app

    