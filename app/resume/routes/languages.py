from flask import request, current_app as app
from .. import token_required, resume_bp
from app.models import Language, Resume
from app import db

@resume_bp.route('/languages/', methods=['POST'])
@token_required
def create_language(current_user):
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
    l = Language(name=data['name'], resume_id=data['resume id'])
    db.session.add(l)
    r.languages.append(l)
    db.session.commit()
    return l.to_dict(), 201

@resume_bp.route('/languages/')
@token_required
def get_languages(current_user):
    return {
        'languages': [{
                'language': [language.to_dict() for language in resume.languages], 
                'resume_id': resume.id
            } for resume in current_user.resumes]
    }

@resume_bp.route('/languages/<int:id>/')
@token_required
def get_language(current_user, id):
    l=Language.query.get_or_404(id)
    if current_user != l.resume.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    return l.to_dict()

@resume_bp.route('/languages/<int:id>/', methods=['PUT'])
@token_required
def update_language(current_user, id):
    l=Language.query.get_or_404(id)
    if current_user != l.resume.users:
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
    l.name=data['name']
    db.session.commit()
    return {
        'success': 'Data updated successfully'
    }

@resume_bp.route('/languages/<int:id>/', methods=['DELETE'])
@token_required
def delete_language(current_user, id):
    l=Language.query.get_or_404(id)
    if current_user != l.resume.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    db.session.delete(l)
    db.session.commit()
    return '', 204