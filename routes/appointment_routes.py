from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.models import db, Appointment, Doctor, Patient

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/appointments')
@login_required
def list_appointments():
    appointments = Appointment.query.order_by(Appointment.id.desc()).all()
    doctors = Doctor.query.all()
    patients = Patient.query.all()
    return render_template('appointments.html', appointments=appointments, doctors=doctors, patients=patients)

@appointment_bp.route('/book', methods=['GET', 'POST'])
@login_required
def book_appointment():
    doctors = Doctor.query.all()
    patients = Patient.query.all()

    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        doctor_id = request.form.get('doctor_id')
        appointment_date = request.form.get('date')
        appointment_time = request.form.get('time')

        doctor = Doctor.query.get_or_404(doctor_id)
        patient = Patient.query.get(patient_id) if patient_id else None

        p_name = patient.full_name if patient else current_user.full_name
        p_id = patient.id if patient else (patients[0].id if patients else 1)

        count = Appointment.query.count() + 1
        appointment_code = f"APT{count:03d}"

        new_apt = Appointment(
            appointment_code=appointment_code,
            patient_id=p_id,
            patient_name=p_name,
            doctor_id=doctor.id,
            doctor_name=f"{doctor.full_name} ({doctor.specialization})",
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status='Scheduled'
        )
        db.session.add(new_apt)
        db.session.commit()

        return redirect(url_for('appointment.booking_success', apt_id=new_apt.id))

    return render_template('appointments.html', doctors=doctors, patients=patients, appointments=Appointment.query.all())

@appointment_bp.route('/appointment/success/<int:apt_id>')
@login_required
def booking_success(apt_id):
    apt = Appointment.query.get_or_404(apt_id)
    return render_template('appointment_success.html', appointment=apt)
