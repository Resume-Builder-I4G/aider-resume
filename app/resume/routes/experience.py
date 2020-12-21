from flask import request, current_app as app
from .. import token_required, resume_bp
from app.models import Experience, Resume
from app import db
import datetime

@resume_bp.route('/experiences/', methods=['POST'])
@token_required
def create_experience(current_user):
    data = request.get_json()
    if not 'job title' in data or not 'resume id' in data or not 'start_year' in data\
        or not 'company' in data:
        return {
            'error': 'Invalid data',
            'message': 'Job title, company, start_year and resume id must be given'
        }, 400
    
    try:
        r = Resume.query.get_or_404(int(data['resume id']))
    except Exception as e:
        return {
            'error': 'Your request can not be processed',
            'message': str(e)
        }, 500
    e = Experience(
        title=data['job title'], resume_id=data['resume id'], 
        start_year=int(data['start_year']), 
        company=data['company'])
    if data.get('description'):
        e.description = data['description']
    if data.get('start_month'):
        e.start_month = int(data['start_month'])
    if data.get('end_year'):
        e.end_year = int(data['end_year'])
        if data.get('end_month'):
            e.end_month = int(data['end_month'])
    db.session.add(e)
    r.experiences.append(e)
    db.session.commit()
    return e.to_dict(), 201

@resume_bp.route('/experiences/')
@token_required
def get_experiences(current_user):
    return {
        'experiences': [{
                'experience': [experience.to_dict() for experience in resume.experiences], 
                'resume_id': resume.id
            } for resume in current_user.resumes]
    }

@resume_bp.route('/experiences/<int:id>/')
@token_required
def get_experience(current_user, id):
    e = Experience.query.get_or_404(id)
    if current_user != e.resume.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    return e.to_dict()

@resume_bp.route('/experiences/<int:id>/', methods=['PUT'])
@token_required
def update_experience(current_user, id):
    e = Experience.query.get_or_404(id)
    if current_user != e.resume.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    data = request.get_json()
    if data.get('course'):
        e.title=data['course']
    if data.get('school'):
        e.title=data['school']
    if data.get('start_year'):
        e.start_year=data['start_year']
    if data.get('end_month'):
        e.end_month=data['end_month']
    if data.get('start_month'):
        e.start_month=data['start_month']
    if data.get('end_year'):
        e.end_year=data['end_year']
    if data.get('description'):
        e.description=data['description']
    db.session.commit()
    return {
        'success': 'Data updated successfully'
    }

@resume_bp.route('/experiences/<int:id>/', methods=['DELETE'])
@token_required
def delete_experience(current_user, id):
    e = Experience.query.get_or_404(id)
    if current_user != e.resume.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    db.session.delete(e)
    db.session.commit()
    return '', 204