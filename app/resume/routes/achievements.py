from flask import request, current_app as app
from .. import token_required, resume_bp
from app.models import Achievement, Resume
from app import db

@resume_bp.route('/achievements/', methods=['POST'])
@token_required
def create_achievement(current_user):
    data = request.get_json()
    if not 'name' in data or not 'resume id' in data:
        return {
            'error': 'Invalid data',
            'message': 'Name and resume id must be given'
        }, 400
    try:
        r = Resume.query.get_or_404(int(data['resume id']))
    except Exception as e:
        return {
            'error': 'Your request can not be processed',
            'message': str(e)
        }, 500
    a = Achievement(name=data['name'], resume_id=data['resume id'])
    db.session.add(a)
    r.achievements.append(a)
    db.session.commit()
    return a.to_dict(), 201

@resume_bp.route('/achievements/')
@token_required
def get_achievements(current_user):
    return {
        'achievements': [{
                'achievement': [achievement.to_dict() for achievement in resume.achievements], 
                'resume_id': resume.id
            } for resume in current_user.resumes]
    }

@resume_bp.route('/achievements/<int:id>/')
@token_required
def get_achievement(current_user, id):
    a=Achievement.query.get_or_404(id)
    if current_user != a.resume.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    return a.to_dict()

@resume_bp.route('/achievements/<int:id>/', methods=['PUT'])
@token_required
def update_achievement(current_user, id):
    a=Achievement.query.get_or_404(id)
    if current_user != a.resume.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    data = request.get_json()
    if not 'name' in data:
        return {
            'error': 'Invalid data',
            'message': 'Name not given'
        }, 400
    a.name=data['name']
    db.session.commit()
    return {
        'success': 'Data updated successfully'
    }

@resume_bp.route('/achievements/<int:id>/', methods=['DELETE'])
@token_required
def delete_achievement(current_user, id):
    a=Achievement.query.get_or_404(id)
    if current_user != a.resume.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    db.session.delete(a)
    db.session.commit()
    return '', 204