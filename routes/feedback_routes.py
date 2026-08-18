from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from models.models import db, PatientFeedback, Doctor, Patient
from datetime import datetime

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['GET'])
@login_required
def feedback_dashboard():
    feedbacks = PatientFeedback.query.order_by(PatientFeedback.created_at.desc()).all()
    doctors = Doctor.query.all()
    
    # Calculate stats
    total_count = len(feedbacks)
    if total_count > 0:
        avg_doc = round(sum(f.doctor_rating for f in feedbacks) / total_count, 1)
        avg_hosp = round(sum(f.hospital_rating for f in feedbacks) / total_count, 1)
        avg_lab = round(sum(f.lab_rating for f in feedbacks) / total_count, 1)
        avg_pharm = round(sum(f.pharmacy_rating for f in feedbacks) / total_count, 1)
        overall_avg = round((avg_doc + avg_hosp + avg_lab + avg_pharm) / 4, 1)
    else:
        avg_doc = avg_hosp = avg_lab = avg_pharm = overall_avg = 5.0

    return render_template(
        'feedback.html',
        feedbacks=feedbacks,
        doctors=doctors,
        total_count=total_count,
        avg_doc=avg_doc,
        avg_hosp=avg_hosp,
        avg_lab=avg_lab,
        avg_pharm=avg_pharm,
        overall_avg=overall_avg
    )

@feedback_bp.route('/feedback/submit', methods=['POST'])
@login_required
def submit_feedback():
    patient_name = request.form.get('patient_name', current_user.full_name)
    doctor_name = request.form.get('doctor_name', 'Dr. Priya Sharma')
    department = request.form.get('department', 'Cardiology')
    doc_rating = int(request.form.get('doctor_rating', 5))
    hosp_rating = int(request.form.get('hospital_rating', 5))
    lab_rating = int(request.form.get('lab_rating', 5))
    pharm_rating = int(request.form.get('pharmacy_rating', 5))
    comments = request.form.get('comments', '')

    new_fb = PatientFeedback(
        patient_name=patient_name,
        doctor_name=doctor_name,
        department=department,
        doctor_rating=doc_rating,
        hospital_rating=hosp_rating,
        lab_rating=lab_rating,
        pharmacy_rating=pharm_rating,
        comments=comments,
        created_at=datetime.utcnow()
    )
    db.session.add(new_fb)
    db.session.commit()
    flash("Thank you! Your feedback has been submitted successfully.", "success")
    return redirect(url_for('feedback.feedback_dashboard'))

@feedback_bp.route('/api/feedback/stats', methods=['GET'])
def feedback_stats_api():
    feedbacks = PatientFeedback.query.all()
    total = len(feedbacks)
    if total == 0:
        return jsonify({"success": True, "total": 0, "overall_avg": 5.0})

    avg_doc = sum(f.doctor_rating for f in feedbacks) / total
    avg_hosp = sum(f.hospital_rating for f in feedbacks) / total
    avg_lab = sum(f.lab_rating for f in feedbacks) / total
    avg_pharm = sum(f.pharmacy_rating for f in feedbacks) / total
    overall_avg = round((avg_doc + avg_hosp + avg_lab + avg_pharm) / 4, 1)

    return jsonify({
        "success": True,
        "total": total,
        "avg_doctor": round(avg_doc, 1),
        "avg_hospital": round(avg_hosp, 1),
        "avg_lab": round(avg_lab, 1),
        "avg_pharmacy": round(avg_pharm, 1),
        "overall_avg": overall_avg
    })
