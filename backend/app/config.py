import os
from datetime import timedelta
from dotenv import load_dotenv


'''
Organises related settings together and uses inheritance
for different environments (development, production, testing).

This parent class contains settings that are shared across
all environments.
'''
class Config:
  '''Base configuration'''

  # Use cases: signing session cookies, CSRF protection
  SECRET_KEY = os.environ.get('SECRET_KEY')

  # Disable SQLAlchemy's event notification system as it
  # can jeopardise performance.
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  # Use case: specifically for signing JWT tokens.
  JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

  # Have the JWT access token expire after one hour.
  JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)