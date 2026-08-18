from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.models import db, Doctor

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/doctors')
@login_required
def list_doctors():
    query = request.args.get('search', '').strip()
    if query:
        doctors = Doctor.query.filter(
            (Doctor.full_name.ilike(f'%{query}%')) | 
            (Doctor.specialization.ilike(f'%{query}%')) |
            (Doctor.department.ilike(f'%{query}%'))
        ).all()
    else:
        doctors = Doctor.query.order_by(Doctor.id.asc()).all()
    return render_template('doctors.html', doctors=doctors, search=query)

@doctor_bp.route('/doctor/add', methods=['POST'])
@login_required
def add_doctor():
    full_name = request.form.get('full_name', '').strip()
    specialization = request.form.get('specialization', '').strip()
    qualification = request.form.get('qualification', '').strip()
    department = request.form.get('department', '').strip()
    phone = request.form.get('phone', '').strip()
    email = request.form.get('email', '').strip()
    available_time = request.form.get('available_time', '').strip()

    count = Doctor.query.count() + 1
    doctor_code = f"DOC{count:03d}"

    new_doctor = Doctor(
        doctor_code=doctor_code,
        full_name=full_name,
        specialization=specialization,
        qualification=qualification,
        department=department,
        phone=phone,
        email=email,
        available_time=available_time
    )
    db.session.add(new_doctor)
    db.session.commit()

    flash(f'Doctor {full_name} added successfully with ID: {doctor_code}', 'success')
    return redirect(url_for('doctor.list_doctors'))

@doctor_bp.route('/doctor/edit/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def edit_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)

    if request.method == 'POST':
        doctor.full_name = request.form.get('full_name', '').strip() or doctor.full_name
        doctor.specialization = request.form.get('specialization', '').strip() or doctor.specialization
        doctor.qualification = request.form.get('qualification', '').strip() or doctor.qualification
        doctor.department = request.form.get('department', '').strip() or doctor.department
        doctor.phone = request.form.get('phone', '').strip() or doctor.phone
        doctor.email = request.form.get('email', '').strip() or doctor.email
        doctor.available_time = request.form.get('available_time', '').strip() or doctor.available_time

        db.session.commit()
        flash(f'Doctor {doctor.full_name} updated successfully.', 'success')
        return redirect(url_for('doctor.list_doctors'))

    doctors = Doctor.query.order_by(Doctor.id.asc()).all()
    return render_template('doctors.html', doctors=doctors, search='', edit_doctor=doctor)

@doctor_bp.route('/doctor/delete/<int:doctor_id>', methods=['POST'])
@login_required
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    db.session.delete(doctor)
    db.session.commit()
    flash('Doctor record deleted successfully.', 'info')
    return redirect(url_for('doctor.list_doctors'))
