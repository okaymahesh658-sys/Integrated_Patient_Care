from flask import Blueprint, render_template
from flask_login import login_required
from models.models import db, Patient, Doctor, Appointment, Medicine, BillingRecord, Notification

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics')
@login_required
def analytics_dashboard():
    total_patients = 520
    total_doctors = 28
    total_appointments = 175
    total_prescriptions = 162
    total_lab_reports = 118
    total_pharmacy_txns = 145

    rbac_matrix = [
        {"role": "Administrator", "users": 5, "permissions": "All Modules & Full System Control", "status": "Active"},
        {"role": "Doctor", "users": 15, "permissions": "Patient Records, Appointment, Consultation, Prescription", "status": "Active"},
        {"role": "Nurse", "users": 10, "permissions": "Patient Registration, Vitals, Appointments", "status": "Active"},
        {"role": "Pharmacist", "users": 7, "permissions": "Pharmacy Inventory, Dispensing, Medicine Stock", "status": "Active"},
        {"role": "Lab Staff", "users": 6, "permissions": "Lab Tests, Upload Reports, Patient Verification", "status": "Active"},
        {"role": "Receptionist", "users": 2, "permissions": "Appointments, Patient Lookup, Reception Billing", "status": "Active"}
    ]

    recent_logs = [
        {"user": "Admin User logged in", "time": "23-07-2026 10:15 AM", "status": "Success"},
        {"user": "Dr. Priya updated patient record", "time": "23-07-2026 09:45 AM", "status": "Success"},
        {"user": "Lab Staff uploaded report (LAB1009)", "time": "23-07-2026 09:20 AM", "status": "Success"},
        {"user": "Pharmacist added medicine stock", "time": "23-07-2026 09:05 AM", "status": "Success"},
        {"user": "Nurse updated vital signs", "time": "23-07-2026 08:50 AM", "status": "Success"}
    ]

    return render_template(
        'analytics.html',
        total_patients=total_patients,
        total_doctors=total_doctors,
        total_appointments=total_appointments,
        total_prescriptions=total_prescriptions,
        total_lab_reports=total_lab_reports,
        total_pharmacy_txns=total_pharmacy_txns,
        rbac_matrix=rbac_matrix,
        recent_logs=recent_logs
    )
