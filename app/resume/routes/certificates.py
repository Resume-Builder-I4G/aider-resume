from flask import request, current_app as app
from .. import token_required, resume_bp
from app.models import Certificate, Resume
from app import db
import datetime

@resume_bp.route('/certificates/', methods=['POST'])
@token_required
def create_certificate(current_user):
    data = request.get_json()
    if not 'name' in data or not 'resume id' in data or not 'year' in data:
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
    c = Certificate(name=data['name'], resume_id=data['resume id'], year=data['year'])
    db.session.add(c)
    r.certificates.append(c)
    db.session.commit()
    return c.to_dict(), 201

@resume_bp.route('/certificates/')
@token_required
def get_certificates(current_user):
    return {
        'certificates': [{
                'certificate': [certificate.to_dict() for certificate in resume.certificates], 
                'resume_id': resume.id
            } for resume in current_user.resumes]
    }

@resume_bp.route('/certificates/<int:id>/')
@token_required
def get_certificate(current_user, id):
    c=Certificate.query.get_or_404(id)
    if current_user != c.resume.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    return c.to_dict()

@resume_bp.route('/certificates/<int:id>/', methods=['PUT'])
@token_required
def update_certificate(current_user, id):
    c=Certificate.query.get_or_404(id)
    if current_user != c.resume.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    data = request.get_json()
    if not 'year' in data and not 'name' in data:
        return {
            'error': 'Invalid data',
            'message': 'Name not given'
        }, 400
    if data.get('name'):
        c.name=data['name']
    if data.get('year'):
        c.year=data['year']
    db.session.commit()
    return {
        'success': 'Data updated successfully'
    }

@resume_bp.route('/certificates/<int:id>/', methods=['DELETE'])
@token_required
def delete_certificate(current_user, id):
    c = Certificate.query.get_or_404(id)
    if current_user != c.resume.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    db.session.delete(c)
    db.session.commit()
    return '', 204