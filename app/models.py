from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from . import db

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(30), index=True)
    email=db.Column(db.String(30), index=True, unique=True)
    password_hash=db.Column(db.String(108))
    is_confirmed=db.Column(db.Boolean, default=False)
    payment=db.Column(db.Boolean, default=False)
    resumes=db.relationship('Resume', backref='users', lazy='dynamic')
   
    def set_password(self, password):
        self.password_hash=generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def get_reset_token(self, expires_sec=1800):
        '''Generates a timed token to reset password'''
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod 
    def verify_reset_token(token):
        '''Verifies the timed token generated in the function above'''
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        '''This functions describes how the user model will be displayed'''
        return f"User('{self.email}')"
    
    def to_dict(self):
        resumes = [resume.to_dict() for resume in self.resumes.all()]
        return {
            'name': self.name, 'email': self.email, 'id': self.id,
            'is_confirmed': self.is_confirmed, 'resumes': resumes,
        }


class Resume(db.Model):
    id=db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, index=True)
    email=db.Column(db.String, index=True)
    avatar=db.Column(db.String, index=True)
    website=db.Column(db.String, index=True)
    phone=db.Column(db.Integer)
    city=db.Column(db.String, index=True)
    state=db.Column(db.String, index=True)
    country=db.Column(db.String, index=True)
    current_job=db.Column(db.String, index=True)
    template_name=db.Column(db.String, index=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skills=db.relationship('Skill', backref='resume', lazy='dynamic')
    languages=db.relationship('Language', backref='resume', lazy='dynamic')
    hobbies=db.relationship('Hobby', backref='resume', lazy='dynamic')
    educations=db.relationship('Education', backref='resume', lazy='dynamic')
    experiences=db.relationship('Experience', backref='resume', lazy='dynamic')
    achievements=db.relationship('Achievement', backref='resume', lazy='dynamic')
    certificates=db.relationship('Certificate', backref='resume', lazy='dynamic')
    
    def to_dict(self):
        skills = [skill.to_dict() for skill in self.skills.all()]
        languages = [language.to_dict() for language in self.languages.all()]
        hobbies = [hobby.to_dict() for hobby in self.hobbies.all()]
        education = [education.to_dict() for education in self.educations.all()]
        experiences = [experience.to_dict() for experience in self.experiences.all()]
        certificates = [certificate.to_dict() for certificate in self.certificates.all()]
        achievements = [achievement.to_dict() for achievement in self.achievements.all()]
        return {
            'id': self.id, 'name': self.name, 'email': self.email, 'avatar': f'http://localhost:5000/static/avatars/{self.avatar}',
            'website': self.website, 'city': self.city, 'state': self.state,
            'country': self.country, 'template name': self.template_name,
            'current_job': self.current_job, 'skills': skills, 'languages': languages,
            'education': education, 'experiences': experiences, 'hobbies': hobbies, 
            'achievements': achievements, 'certificates': certificates
        }
    
    def __repr__(self):
        '''This functions describes how the user model will be displayed'''
        return f"Resume('{self.name}': {self.id})"

class Experience(db.Model):
    '''
        Job representation in the database. 
        The many side of a many-to-many relationship with user model
    '''
    id = db.Column(db.Integer, primary_key=True)
    company=db.Column(db.String)
    title=db.Column(db.String)
    description=db.Column(db.Text)
    start_year=db.Column(db.Integer)
    end_year=db.Column(db.Integer)
    start_month=db.Column(db.Integer)
    end_month=db.Column(db.Integer)
    resume_id=db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)

    def __repr__(self):
        '''This functions describes how the user model will be displayed'''
        return f"Job('{self.company}': '{self.start_date} - {self.end_date}')"
    
    def to_dict(self):
        data = {
            'id': self.id, 'company': self.company,  
            'title': self.title, 'start_year': self.start_year
        }
        if self.start_month:
            data['start_month']=self.start_month
        if self.end_month:
            data['end_month']=self.end_month
        if self.end_year:
            data['end_year']=self.end_year
        if self.description:
            data['description']= self.description
        return data

    def __repr__(self):
        '''This functions describes how the user model will be displayed'''
        return f"Experience('{self.name}': {self.resume.name})"
    

class Education(db.Model):
    '''
        Education representation in the database. 
        The many side of a one-to-many relationship with user model
    '''
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(30), nullable=False)
    description=db.Column(db.Text)
    school=db.Column(db.String(30), nullable=False)
    start_year=db.Column(db.Integer)
    end_year=db.Column(db.Integer)
    start_month=db.Column(db.Integer)
    end_month=db.Column(db.Integer)
    resume_id=db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)

    def __repr__(self):
        '''This functions describes how the user model will be displayed'''
        return f"Education('{self.title}', '{self.start_date} - {self.end_date}')"
    
    def to_dict(self):
        data = {
            'id': self.id, 'school': self.school,  
            'title': self.title, 'start_year': self.start_year
        }
        if self.start_month:
            data['start_month']=self.start_month
        if self.end_month:
            data['end_month']=self.end_month
        if self.end_year:
            data['end_year']=self.end_year
        if self.description:
            data['description']= self.description
        return data

class Language(db.Model):
    '''Language representation in the database. The many side of a one-to-many relationship with user model'''
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30), nullable=False)
    resume_id=db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)

    def __repr__(self):
        '''This functions describes how the user model will be displayed'''
        return f"Interest('{self.name}')"
    
    def to_dict(self):
        return {
            'id': self.id, 'name': self.name
        }

class Skill(db.Model):
    '''Skill representation in the database. The many side of a one-to-ma   ny relationship with user model'''
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30), nullable=False)
    level=db.Column(db.String(15))
    resume_id=db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)

    def __repr__(self):
        '''This functions describes how the user model will be displayed'''
        return f"skill('{self.name}')"
    
    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'level': self.level
        }

class Hobby(db.Model):
    '''Hobby representation in the database. The many side of a one-to-many relationship with user model'''
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30), nullable=False)
    resume_id=db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)

    def __repr__(self):
        return f"Hobby('{self.name}')"

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name
        }

class Achievement(db.Model):
    '''Achievement representation in the database. The many side of a one-to-many relationship with user model'''
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30), nullable=False)
    resume_id=db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    
    def __repr__(self):
        return f"Achievement('{self.name}')"
    
    def to_dict(self):
        return {
            'id': self.id, 'name': self.name
        }

class Certificate(db.Model):
    '''Certificate representation in the database. The many side of a one-to-many relationship with user model'''
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30), nullable=False)
    year=db.Column(db.Integer)
    resume_id=db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    
    def __repr__(self):
        return f"Certificate('{self.name}')"

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'year': self.year
        }

