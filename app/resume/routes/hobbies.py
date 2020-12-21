from flask import request, current_app as app
from .. import token_required, resume_bp
from app.models import Hobby, Resume
from app import db

@resume_bp.route('/hobbies/', methods=['POST'])
@token_required
def create_hobby(current_user):
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
    h = Hobby(name=data['name'], resume_id=data['resume id'])
    db.session.add(h)
    r.hobbies.append(h)
    db.session.commit()
    return h.to_dict(), 201

@resume_bp.route('/hobbies/')
@token_required
def get_hobbies(current_user):
    return {
        'hobbies': [{
                'hobby': [hobby.to_dict() for hobby in resume.hobbies], 
                'resume_id': resume.id
            } for resume in current_user.resumes]
    }

@resume_bp.route('/hobbies/<int:id>/')
@token_required
def get_hobby(current_user, id):
    h=Hobby.query.get_or_404(id)
    if current_user != h.resume.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    return h.to_dict()

@resume_bp.route('/hobbies/<int:id>/', methods=['PUT'])
@token_required
def update_hobby(current_user, id):
    h=Hobby.query.get_or_404(id)
    if current_user != h.resume.users:
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
    h.name=data['name']
    db.session.commit()
    return {
        'success': 'Data updated successfully'
    }

@resume_bp.route('/hobbies/<int:id>/', methods=['DELETE'])
@token_required
def delete_hobby(current_user, id):
    h=Hobby.query.get_or_404(id)
    if current_user != h.resume.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    db.session.delete(h)
    db.session.commit()
    return '', 204