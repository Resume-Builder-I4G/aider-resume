from flask import Flask, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
import jwt

db = SQLAlchemy()
mail = Mail()
migrate = Migrate()

from app import models

def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.from_object(config)
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from .users import users_bp
    app.register_blueprint(users_bp, url_prefix='/api/v2/users')

    from .resume import resume_bp
    app.register_blueprint(resume_bp, url_prefix='/api/v2/resumes')

    return app