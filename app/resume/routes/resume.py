import os
from typing import List, Dict
from app import db
from app.email import send_mail
from app.models import Resume, User
from flask import (
    current_app as app, render_template, make_response, request
)

from .. import resume_bp, token_required
from .utils import save_pic, html_to_pdf 


@resume_bp.route('/', methods=['POST'])
@token_required
def create_resume(current_user: User) -> dict:
    try:
        data: Dict[str: str] = request.form
        if not 'name' in data or not 'email' in data or not 'phone' in data \
            or not 'state' in data  or not 'country' in data:
            return {
                'error': 'Invalid data',
                'message': 'Name, email, phone, state, country must be given'
            }, 400
        templates: List[str]=['a', 'b'] # add the list of available templates
        if 'template name' not in data or data['template name'] not in templates:
            return {
                'error': 'Invalid data',
                'message': 'Invalid template'
            }, 400
    except Exception as e:
        return {
            'error': 'Bad input',
            'message': str(e)
        }
    r = Resume(
        name=data['name'], email=data['email'], 
        phone=int(data['phone'].replace('+', '')), state=data['state'],
        country=data['country'], template_name=data['template name'], 
        user_id=current_user.id
        )
    if data.get('current job'):
        r.current_job=data['current job']
    if data.get('website'):
        # validate input
        r.website=data['website']
    if data.get('city'):
        # validate input
        r.city=data['city']
    if request.files.get('avatar'):
        avatar=save_pic(request.files['avatar'])
        if type(avatar) == dict:
            return {
                'error': 'Invalid data',
                'message': avatar['message']
            }, 400
        r.avatar = avatar
    
    db.session.add(r)
    db.session.commit()
    return r.to_dict(), 201

@resume_bp.route('/') 
@token_required
def get_resumes(current_user):
    return {
        'user': {
            'name': current_user.name, 
            'email': current_user.email, 
            'id': current_user.id
        },
        'resumes': [
            resume.to_dict() for resume in current_user.resumes
        ]
    }

@resume_bp.route('/<int:id>/')
@token_required
def get_resume(current_user, id):
    r=Resume.query.get_or_404(id)
    if current_user != r.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    return r.to_dict()

@resume_bp.route('/<int:id>/', methods=['PUT'])
@token_required
def update_resume(current_user, id):
    r=Resume.query.get_or_404(id)
    if current_user != r.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    if request.form:
        data = request.form
        templates:List[str]=['a', 'b']
        if 'template name' in data and data['template name'] not in templates:
            return {
                'error': 'Invalid data',
                'message': 'Invalid template'
            }, 400
        if data.get('name'):
            # validate input
            r.name=data['name']
        if data.get('email'):
            # validate input
            r.email=data['email']
        if data.get('city'):
            # validate input
            r.city=data['city']
        if data.get('website'):
            # validate input
            r.website=data['website']
        if data.get('phone'):
            # validate input
            r.phone=data['phone']
        if data.get('state'):
            # validate input
            r.state=data['state']
        if data.get('country'):
            # validate input
            r.country=data['country']
        if data.get('current_job'):
            # validate input
            r.current_job=data['current_job']
        if data.get('template name'):
            # validate input
            r.template_name=data['template name']
    if request.files.get('avatar'):
        if r.avatar:
            os.remove(os.path.join(app.root_path, 'static', 'avatars', r.avatar))
        avatar=save_pic(request.files['avatar'])
        if type(avatar) == dict:
            return avatar, 400
        r.avatar = avatar
    db.session.commit()
    return {
        'success': 'Data updated successfully'
    }

@resume_bp.route('/<int:id>/', methods=['DELETE'])
@token_required
def delete_resume(current_user, id):
    r=Resume.query.get_or_404(id)
    if current_user != r.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    db.session.delete(r)
    db.session.commit()
    return '', 204

def resume_downloader(r):
    templates = {
        'a': 'template-A'
    }
    style=os.path.join(app.root_path,
            f'static/Resume-Templates/{templates[r.template_name]}/style.css'
        )
    template=render_template(
        f'Resume-Templates/{templates[r.template_name]}/index.html',
        user=r.users, 
        resume=r
    )
    css=[style]
    pdf=make_response(html_to_pdf(template, *css))
    pdf.headers['Content-Type'] = 'application/pdf'
    pdf.headers['Content-Disposition'] = f'inline; {r.users.name}.pdf'
    return pdf

@resume_bp.route('/download/<int:id>/')
@token_required
def download_resume(current_user, id):
    r=Resume.query.get_or_404(id)
    if current_user != r.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    pdf = resume_downloader(r)
    return pdf

@resume_bp.route('/mail/<int:id>/')
@token_required
def get_resume_in_mail(current_user, id):
    r=Resume.query.get_or_404(id)
    if current_user != r.users:
        return {
            'error': 'Forbidden',
            'message': 'You do not have access to that!'
        }, 403
    pdf = resume_downloader(r)
    send_mail(
            [current_user.email], 'Here is your resume', 
            'mail/reset_password', attachments=pdf , u=current_user
        )

