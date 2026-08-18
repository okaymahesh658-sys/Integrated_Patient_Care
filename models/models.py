from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(50))
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Patient') # Admin, Doctor, Nurse, Patient
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    patient_code = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150))
    blood_group = db.Column(db.String(10), nullable=False)
    address = db.Column(db.Text, nullable=False)
    medical_history = db.Column(db.Text, default='No known allergies')
    chronic_diseases = db.Column(db.String(255), default='None')
    current_medication = db.Column(db.String(255), default='None')
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship('Appointment', backref='patient_rel', lazy=True)

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    doctor_code = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    available_time = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship('Appointment', backref='doctor_rel', lazy=True)

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    appointment_code = db.Column(db.String(20), unique=True, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    patient_name = db.Column(db.String(150), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    doctor_name = db.Column(db.String(150), nullable=False)
    appointment_date = db.Column(db.String(20), nullable=False)
    appointment_time = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='Scheduled') # Scheduled, Confirmed, Completed, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TextSummary(db.Model):
    __tablename__ = 'text_summaries'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(150), nullable=False)
    original_text = db.Column(db.Text, nullable=False)
    summary_text = db.Column(db.Text, nullable=False)
    model_used = db.Column(db.String(50), nullable=False)
    summary_length = db.Column(db.String(20), nullable=False)
    reference_summary = db.Column(db.Text, default='')
    rouge_scores = db.Column(db.Text, default='{}')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TextParaphrase(db.Model):
    __tablename__ = 'text_paraphrases'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(150), nullable=False)
    original_text = db.Column(db.Text, nullable=False)
    paraphrased_options = db.Column(db.Text, nullable=False)
    model_used = db.Column(db.String(50), nullable=False)
    creativity = db.Column(db.Float, nullable=False, default=1.0)
    complexity_level = db.Column(db.String(50), nullable=False)
    rouge_scores = db.Column(db.Text, default='[]')
    readability_scores = db.Column(db.Text, default='[]')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TextReadabilityFile(db.Model):
    __tablename__ = 'text_readability_files'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(150), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    filetype = db.Column(db.String(50), nullable=False)
    filesize = db.Column(db.Integer, nullable=False)
    filedata = db.Column(db.Text, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class PatientFeedback(db.Model):
    __tablename__ = 'patient_feedback'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=True)
    patient_name = db.Column(db.String(150), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=True)
    doctor_name = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100), nullable=False, default='General Medicine')
    doctor_rating = db.Column(db.Integer, nullable=False, default=5)
    hospital_rating = db.Column(db.Integer, nullable=False, default=5)
    lab_rating = db.Column(db.Integer, nullable=False, default=5)
    pharmacy_rating = db.Column(db.Integer, nullable=False, default=5)
    comments = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)




