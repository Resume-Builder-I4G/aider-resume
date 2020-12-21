import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL') or 'sqlite:///app.db'
    SECRET_KEY=os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    # MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    # MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
    MAIL_SERVER=os.getenv('MAIL_SERVER')
    MAIL_PORT=os.getenv('MAIL_PORT')
    # MAIL_USE_TLS=os.getenv('MAIL_USE_TLS')
    PDF_TO_HTML=os.environ.get('PDF_TO_HTML')

class TestConfig:
    TESTING=True
    SQLALCHEMY_DATABASE_URI='sqlite:///test.db'
    SECRET_KEY=os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    MAIL_SERVER='localhost'
    MAIL_PORT=1025
    # MAIL_USE_TLS=os.getenv('MAIL_USE_TLS')
    PDF_TO_HTML=os.environ.get('PDF_TO_HTML')