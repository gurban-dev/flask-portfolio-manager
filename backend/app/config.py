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
  '''Base configuration class.'''

  # Use cases: signing session cookies, CSRF protection
  SECRET_KEY = os.environ.get('SECRET_KEY')

  # Disable SQLAlchemy's event notification system as it
  # can jeopardise performance.
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  # Use case: specifically for signing JWT tokens.
  # Verifies token signatures when users make authenticated
  # requests.
  JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

  # Have the JWT access token expire after one hour.
  JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

  # The following line is needed because it specifies which frontend
  # URL can make requests to the API.

  # Cross-origin resource sharing.

  # First the program tries to obtain a FRONTEND_URL from .env.
  # If there is no such FRONTEND_URL in .env, it falls back to
  # the second argument ('http://localhost:3000').
  CORS_ORIGINS = os.environ.get('FRONTEND_URL', 'http://localhost:3000')

  # The next line makes it possible to connect to the Redis server.
  # Redis is an in-memory data store used for:
  # Caching, Session storage, Message broker for Celery (background tasks)
  REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

  # Tell Celery where to store task messages.
  # Celery is a distributed task queue for running background jobs.
  CELERY_BROKER_URL = REDIS_URL

  # Celery needs to know where to store the results.
  # The results are return values of completed tasks.
  CELERY_RESULT_BACKEND = REDIS_URL


class DevelopmentConfig(Config):
  """Development Configuration"""
  DEBUG = True

  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite://dev.db'

  SQLALCHEMY = True


class ProductionConfig(Config):
  """Development Configuration"""
  DEBUG = False

  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

  # Security headers
  SESSION_COOKIE_SECURE = True
  SESSION_COOKIE_HTTPONLY = True
  SESSION_COOKIE_SAMESITE = 'Lax'


class TestingConfig(Config):
  """Testing Configuration"""
  TESTING = True

  SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
  
  JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)

config = {
  'development': DevelopmentConfig,
  'production': ProductionConfig,
  'testing': TestingConfig,
  'default':DevelopmentConfig
}