import jwt
from flask import Blueprint, request, current_app, jsonify
from app import models

users_bp = Blueprint('users', __name__)

from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
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
        except Exception as e:
            return jsonify({
                'error': 'Something went wrong',
                'message': str(e)
                }), 500

        return f(current_user, *args, **kwargs)

    return decorated

from . import views
