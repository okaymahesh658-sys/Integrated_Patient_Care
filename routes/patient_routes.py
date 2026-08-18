from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.models import db, Patient, Appointment

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/patients')
@login_required
def list_patients():
    patients = Patient.query.order_by(Patient.id.desc()).all()
    return render_template('patients.html', patients=patients)

@patient_bp.route('/patient/register', methods=['POST'])
@login_required
def register_patient():
    full_name = request.form.get('full_name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    phone = request.form.get('phone')
    email = request.form.get('email')
    blood_group = request.form.get('blood_group')
    address = request.form.get('address')
    medical_history = request.form.get('medical_history', 'No known allergies')

    count = Patient.query.count() + 1
    patient_code = f"P{count:03d}"

    new_patient = Patient(
        patient_code=patient_code,
        full_name=full_name,
        age=int(age),
        gender=gender,
        phone=phone,
        email=email,
        blood_group=blood_group,
        address=address,
        medical_history=medical_history
    )
    db.session.add(new_patient)
    db.session.commit()

    flash(f'Patient {full_name} registered successfully with ID: {patient_code}', 'success')
    return redirect(url_for('patient.list_patients'))

@patient_bp.route('/patient/<int:patient_id>')
@login_required
def view_patient_profile(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    appointments = Appointment.query.filter_by(patient_id=patient.id).order_by(Appointment.id.desc()).all()
    return render_template('patient_profile.html', patient=patient, appointments=appointments)

@patient_bp.route('/patient/edit/<int:patient_id>', methods=['POST'])
@login_required
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    patient.full_name = request.form.get('full_name')
    patient.age = int(request.form.get('age'))
    patient.gender = request.form.get('gender')
    patient.phone = request.form.get('phone')
    patient.email = request.form.get('email')
    patient.blood_group = request.form.get('blood_group')
    patient.address = request.form.get('address')
    patient.medical_history = request.form.get('medical_history')

    db.session.commit()
    flash('Patient profile updated successfully!', 'success')
    return redirect(url_for('patient.view_patient_profile', patient_id=patient.id))

@patient_bp.route('/patient/delete/<int:patient_id>', methods=['POST'])
@login_required
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient record deleted successfully.', 'info')
    return redirect(url_for('patient.list_patients'))
