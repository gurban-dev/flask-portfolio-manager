from flask import Blueprint, request, jsonify
from flask_jwt_extended import ( 
  create_access_token, create_refresh_token,
  jwt_required, get_jwt_identity
)

from app import db
from app.model.user import User

# Schema defines how the data should be structures.

# fields defines the type of each field in the data.
# E.g. fields.Str, fields.Integer

# validate lets you attach validation rules to fields.
# E.g. max length, range, or custom validators.
from marshmallow import Schema, fields, ValidationError

auth_bp = Blueprint('auth', __name__)


class RegisterSchema(Schema):
  email = fields.Email(requried=True)
  password = fields.Str(required=True, validate=lambda p: len(p) >= 8)
  full_name = fields.Str()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
  """Register a new user. Handles both GET and POST."""

  if request.method == 'GET':
    # Return registration form information.

    '''
    jsonify converts Python data structures into a JSON response that
    can be returned by the API endpoints.
    jsonify is often used when building RESTful APIs.
    
    data = {"message": "Hello, world!", "status": "success"}
    return jsonify(data)

    or

    return jsonify(message="Hello", status="success")

    jsonify converts the Python dictionary data into a JSON response:
    {
      "message": "Hello, world!",
      "status": "success"
    }
    Content-Type: application/json
    '''

    return jsonify({
      'message': 'Registration endpoint',
      'method': 'POST',
      'required_fields': {
        'email': 'string (valid email format)',
        'password': 'string (minimum of 8 characters, must contain \
                     uppercase, lowercase, and digit)'
      },
      'optional_fields': {
        'full_name': 'string (max 100 characters)',
        'default_currency': 'string (EUR, USD, GBP, NOK, SEK)'
      },
      'example': {
        'email': 'user@example.com',
        'password': 'SecurePass123',
        'full_name': 'Alexander Hamilton',
        'default_currency': 'EUR'
      }
    }), 200
  
  # Handle POST requests.
  try:
    # Validate the request data.
    data = RegisterSchema.load(request.json)
  except ValidationError as err:
    return jsonify({'errors': err.messages}), 400
  
  # Check if the user already exists.
  if User.query.filter_by(email=data['email']).first():
    return jsonify({'error': 'Email already registered'}), 409


  schema = RegisterSchema