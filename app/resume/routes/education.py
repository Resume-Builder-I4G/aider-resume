from flask import request, current_app as app
from .. import token_required, resume_bp
from app.models import Education, Resume
from app import db
import datetime

@resume_bp.route('/educations/', methods=['POST'])
@token_required
def create_education(current_user):
    data = request.get_json()
    if not 'course' in data or not 'resume id' in data or not 'start_year' in data\
        or not 'school' in data:
        return {
            'error': 'Invalid data',
            'message': 'course, school, start_year and resume id must be given'
        }, 400
    try:
        r = Resume.query.get_or_404(int(data['resume id']))
    except Exception as e:
        return {
            'error': 'Your request can not be processed',
            'message': str(e)
        }, 500
    e = Education(
        title=data['course'], resume_id=data['resume id'], 
        start_year=data['start_year'],
        school=data['school'])
    if data.get('description'):
        e.description = data['description']
    if data.get('start_month'):
        e.start_month = int(data['start_month'])
    if data.get('end_year'):
        e.end_year = int(data['end_year'])
        if data.get('end_month'):
            e.end_month = int(data['end_month'])
    db.session.add(e)
    r.educations.append(e)
    db.session.commit()
    return e.to_dict(), 201

@resume_bp.route('/educations/')
@token_required
def get_educations(current_user):
    return {
        'educations': [{
                'education': [education.to_dict() for education in resume.educations], 
                'resume_id': resume.id
            } for resume in current_user.resumes]
    }

@resume_bp.route('/educations/<int:id>/')
@token_required
def get_education(current_user, id):
    e=Education.query.get_or_404(id)
    if current_user != e.resume.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    return e.to_dict()

@resume_bp.route('/educations/<int:id>/', methods=['PUT'])
@token_required
def update_education(current_user, id):
    e=Education.query.get_or_404(id)
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

@resume_bp.route('/educations/<int:id>/', methods=['DELETE'])
@token_required
def delete_education(current_user, id):
    e = Education.query.get_or_404(id)
    if current_user != e.resume.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    db.session.delete(e)
    db.session.commit()
    return '', 204