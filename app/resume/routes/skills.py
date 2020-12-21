from flask import request, current_app as app
from .. import token_required, resume_bp
from app.models import Skill, Resume
from app import db

@resume_bp.route('/skills/', methods=['POST'])
@token_required
def create_skill(current_user):
    data = request.get_json()
    if not 'name' in data or not 'resume id' in data or not 'level' in data:
        return {
            'error': 'Invalid data',
            'message': 'Name, level and resume id must be given'
        }, 400
    try:
        print(id)
        r = Resume.query.get_or_404(int(data['resume id']))
    except Exception as e:
        return {
            'error': 'Your request can not be processed',
            'message': str(e)
        }, 500
    s = Skill(name=data['name'], level=data['level'], resume_id=data['resume id'])
    db.session.add(s)
    r.skills.append(s)
    db.session.commit()
    return s.to_dict(), 201

@resume_bp.route('/skills/')
@token_required
def get_skills(current_user):
    return {
        'skills': [{
                'skill': [skill.to_dict() for skill in resume.skills], 
                'resume_id': resume.id
            } for resume in current_user.resumes]
    }

@resume_bp.route('/skills/<int:id>/')
@token_required
def get_skill(current_user, id):
    s: Skill =Skill.query.get_or_404(id)
    if current_user != s.resume.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    return s.to_dict()

@resume_bp.route('/skills/<int:id>/', methods=['PUT'])
@token_required
def update_skill(current_user, id):
    s: Skill =Skill.query.get_or_404(id)
    if current_user != s.resume.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    data = request.get_json()
    if not 'name' in data and not 'level' in data:
        return {
            'error': 'Invalid data',
            'message': 'Name not given'
        }, 400
    if data.get('name'):
        s.name=data['name']
    if data.get('level'): 
        s.level=data['level']
    db.session.commit()
    return {
        'success': 'Data updated successfully'
    }

@resume_bp.route('/skills/<int:id>/', methods=['DELETE'])
@token_required
def delete_skill(current_user, id):
    s: Skill = Skill.query.get_or_404(id)
    if current_user != s.resume.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    db.session.delete(s)
    db.session.commit()
    return '', 204