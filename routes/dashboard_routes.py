from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.models import Patient, Doctor, Appointment, User

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    total_patients = Patient.query.count()
    total_doctors = Doctor.query.count()
    total_nurses = User.query.filter_by(role='Nurse').count()
    today_appointments = Appointment.query.count()

    recent_patients = Patient.query.order_by(Patient.id.desc()).limit(5).all()
    recent_appointments = Appointment.query.order_by(Appointment.id.desc()).limit(5).all()

    return render_template(
        'dashboard.html',
        patients=total_patients,
        doctors=total_doctors,
        nurses=total_nurses,
        appointments=today_appointments,
        recent_patients=recent_patients,
        recent_appointments=recent_appointments,
        user=current_user
    )

@dashboard_bp.route('/reports')
@login_required
def reports():
    total_patients = Patient.query.count()
    total_doctors = Doctor.query.count()
    total_appointments = Appointment.query.count()
    return render_template('reports.html', patients=total_patients, doctors=total_doctors, appointments=total_appointments)
