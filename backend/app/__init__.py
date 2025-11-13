# Flask application factory pattern.

# This __init__.py file exists because it's what makes
# the "app" directory an importable package.

# Import the core Flask class that represents the WSGI
# (Web Server Gateway Interface) application instance.
from flask import Flask

# SQLAlchemy is an ORM (Object-Relational Mapper) whose
# purpose is to interact with a database using Python
# objects instead of raw SQL.
from flask_sqlalchemy import SQLAlchemy

# Migrate makes it possible to change the database schema
# when you change one of your models.
from flask_migrate import Migrate

# Imports JWT (JSON Web Token) authentication manager.
from flask_jwt_extended import JWTManager

# CORS handles Cross-Origin Resource Sharing by giving the
# frontend permission to talk to the backend through requests.
from flask_cors import CORS

# Enables WebSocket support for a bidirectional communication
# channel so that the server can push data to the clients.
from flask_socketio import SocketIO

# Create an instance of the Object-Relational Mapper.
db = SQLAlchemy()

migrate = Migrate()
jwt = JWTManager()
socketio = SocketIO()

def create_app():
  # Create the Flask application instance.
  app = Flask(__name__)

  # Load configuration from a config class.
  app.config.from_object(f'app.config.{config_name.capitalize()}Config')

  # Make the database become aware of this app.
  db.init_app(app)

  migrate.init_app(app, db)

  jwt.init_app(app)

  CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

  socketio.init_app(app, cors_allowed_origins="*")

  from app.resources.auth import auth_bp
  from app.resources.portfolio import portfolio_bp
  from app.resources.analytics import analytics_bp

  app.register_blueprint(auth_bp, url_prefix='/api/auth')
  app.register_blueprint(portfolio_bp, url_prefix='/api/portfolio')
  app.register_blueprint(analytics_bp, url_prefix='/api/analytics')

  return app

create_app()