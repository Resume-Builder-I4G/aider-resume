import jwt
from flask import Blueprint, request, jsonify, current_app

resume_bp = Blueprint('resume', __name__)

from app import models
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(' ')[1]
            except Exception as e:
                return {
                    'error': 'Invalid header',
                    'message': 'You did not provide a valid header.'
                }, 401
        if not token: 
            return jsonify({
                'error': 'Unauthorized',
                'message': 'You did not provide a token'
                }), 401
        try:
            data=jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user=models.User.query.get_or_404(int(data['user_id']))
            if current_user is None:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'Invalid token'
                }), 401
            if not current_user.is_confirmed:
                return jsonify({
                    'error': 'Forbidden',
                    'message': 'You need to confirm your account to perform that operation'
                }), 403
        except Exception as e:
            return jsonify({
                'error': 'Something went wrong',
                'message': str(e)
                }), 500

        return f(current_user, *args, **kwargs)

    return decorated

from .routes import (
    achievements, certificates, education, experience, 
    hobbies, languages, resume, skills
)