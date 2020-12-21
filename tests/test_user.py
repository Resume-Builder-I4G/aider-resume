import unittest
from app import create_app, db
from flask import url_for
from ..app.models import User
from config import TestConfig

class TestUser(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_user_endpoint(self):
        response = self.client.get(url_for('user.get_user'))
        self.assertTrue('error'in response.get_json())