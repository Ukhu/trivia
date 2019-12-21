import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question =  {
            'question': 'Who is the greatest soccer player?',
            'answer': 'Cristiano Ronaldo',
            'difficulty': 1,
            'category': 6,
        }

        self.new_question2 =  {
            'question': 'Which continent is Uganda',
            'answer': 'Africa',
            'difficulty': 1,
            'category': 3,
        }

        self.invalid_question =  {
            'difficulty': 1,
            'category': 6,
        }

        self.search_term = {
            'searchTerm': 'soccer'
        }

        self.play_quiz_params = {
            'previous_questions': [],
            'quiz_category': {'type': 'Sports', 'id': 6}
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'successfully fetched all categories')
        self.assertTrue(data['categories'])
    
    def test_post_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'successfully created a question')
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['created_question']), int)

    def test_400_post_invalid_question(self):
        res = self.client().post('/questions', json=self.invalid_question)
        data = json.loads(res.data)

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'bad request')
        self.assertEqual(data['success'], False)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'successfully fetched questions')
        self.assertTrue(data['questions'])
        self.assertTrue(type(data['total_questions']), int)
        self.assertTrue(data['categories'])

    def test_404_get_questions_with_wrong_page_number(self):
        res = self.client().get('/questions?page=50')
        data = json.loads(res.data)

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        init_res = self.client().post('/questions', json=self.new_question2)
        question_to_delete = json.loads(init_res.data)['created_question']

        res = self.client().delete(f'/questions/{question_to_delete}')
        data = json.loads(res.data)

        deleted_question = Question.query.filter_by(id=question_to_delete).one_or_none()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'successfully deleted question')
        self.assertEqual(deleted_question, None)

    def test_405_unallowed_method(self):
        res = self.client().post(f'/questions/404')
        data = json.loads(res.data)

        self.assertEqual(data['status'], 405)
        self.assertEqual(data['message'], 'method not allowed')
        self.assertEqual(data['success'], False)

    def test_404_delete_non_existent_question(self):
        res = self.client().delete(f'/questions/404')
        data = json.loads(res.data)

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['success'], False)

    def test_search_questions(self):
        res = self.client().post('/questions/search', json=self.search_term)
        data = json.loads(res.data)

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'successfully found questions')
        self.assertTrue(data['questions'])

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/6/questions')
        data = json.loads(res.data)

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'successfully returned questions by category')
        self.assertTrue(data['questions'])

    def test_play_quiz(self):
        res = self.client().post('/quizzes', json=self.play_quiz_params)
        data = json.loads(res.data)

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'successfully returned questions by category')
        self.assertTrue(data['question'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()