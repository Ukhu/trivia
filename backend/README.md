# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Follow the information in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for setting up a virtual environment on your platform.

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API Reference

```

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

Endpoints
GET '/categories'
GET '/questions'
DELETE '/questions/<question_id>'
POST '/questions'
POST '/questions/search'
GET '/categories/<category_id>/questions'
POST '/quizzes'

GET '/categories'
- Fetches all question categories
- Request Arguments: None
- Response:
{
  "success": true,
  "status": 200,
  "message": successfully fetched all categories
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ]
}

GET '/questions'
- Fetches all questions and categories
- Request Arguments: None
- Response:
{
  "success": true,
  "status': 200,
  "message": "successfully fetched questions",
  "questions": [
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
  ],
  "total_questions": 2,
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
  ]
}

DELETE '/questions/<question_id>'
- Deletes the question with the specified id
- Request Arguments: question_id
- Response:
{
  "success": true,
  "status": 200,
  "message": "successfully deleted question"
}

POST '/questions'
- Creates a new question based on the request body
- Request Body: {
    "question": "Who is greatest soccer player in the world?",
    "answer": "Cristiano Ronaldo",
    "difficulty": 1,
    "category": 6
  }
- Response:
{
  "success": true,
  "status": 201,
  "message": "successfully created a question",
  "created_question": 28 #new question id
}

POST '/questions/search'
- Fetches all questions that contain the search term
- Request Body: {
    'searchTerm': 'Paintings'
  }
- Response
{
  "success": true,
  "status": 200,
  "message": "successfully found questions",
  "questions": [
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ]
}

GET '/categories/<category_id>/questions'
- Fetches all questions for the specified category
- Request Arguments: category_id
- Response:
{
  "success": true,
  "status": 200,
  "message": "successfully returned questions by category",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    }
  ]
}

POST '/quizzes'
- Fetches a random question when playing the trivia
- Request Body: {
	"previous_questions": [],
	"quiz_category": {
		"type": "History",
		"id": 4
	}
} 
- Response:
{
  "question": {
    "answer": "George Washington Carver",
    "category": 4,
    "difficulty": 2,
    "id": 12,
    "question": "Who invented Peanut Butter?"
  }
}

The server returns these types of errors

400 - Bad Request
  {
    "success": false, 
    "error": 400,
    "message": "bad request"
  }

404 - Resource Not Found
  {
    "success": false, 
    "error": 404,
    "message": "resource not found"
  }

422 - Unprocessable entity
  {
    "success": false, 
    "error": 422,
    "message": "unprocessable
  }

405 - Method not allowed
  {
    "success": false, 
    "error": 405,
    "message": "Method not allowed"
  }

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```