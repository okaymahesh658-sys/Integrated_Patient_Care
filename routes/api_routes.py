from flask import Blueprint, render_template, jsonify, request
from models.models import db, Patient, Doctor, Appointment, Medicine, BillingRecord, Notification
import time

api_bp = Blueprint('api', __name__)

# REST API Dashboard View
@api_bp.route('/api-dashboard')
def api_dashboard():
    return render_template('rest_api.html')

# REST API Endpoints
@api_bp.route('/api/patients', methods=['GET', 'POST'])
def api_patients():
    start = time.time()
    if request.method == 'POST':
        data = request.json or {}
        p = Patient(
            patient_code=f"P{Patient.query.count()+1:03d}",
            full_name=data.get('name', 'Sample Patient'),
            age=data.get('age', 30),
            gender=data.get('gender', 'Male'),
            phone=data.get('phone', '9876543210'),
            email=data.get('email', 'patient@example.com'),
            blood_group=data.get('blood_group', 'O+'),
            address=data.get('address', 'Chennai, Tamil Nadu')
        )
        db.session.add(p)
        db.session.commit()
        latency = round((time.time() - start) * 1000, 2)
        return jsonify({"status": "success", "message": "Patient created successfully", "latency_ms": latency, "data": {"id": p.id, "patient_code": p.patient_code}}), 201

    patients = Patient.query.all()
    result = [{"id": p.id, "patient_id": p.patient_code, "name": p.full_name, "age": p.age, "gender": p.gender, "phone": p.phone, "email": p.email} for p in patients]
    latency = round((time.time() - start) * 1000, 2)
    return jsonify({"status": "success", "count": len(result), "latency_ms": latency, "data": result})

@api_bp.route('/api/doctors', methods=['GET'])
def api_doctors():
    start = time.time()
    doctors = Doctor.query.all()
    result = [{"id": d.id, "doctor_code": d.doctor_code, "name": d.full_name, "specialization": d.specialization, "department": d.department, "available_time": d.available_time} for d in doctors]
    latency = round((time.time() - start) * 1000, 2)
    return jsonify({"status": "success", "count": len(result), "latency_ms": latency, "data": result})

@api_bp.route('/api/consultations', methods=['GET'])
def api_consultations():
    start = time.time()
    latency = round((time.time() - start) * 1000, 2)
    return jsonify({"status": "success", "latency_ms": latency, "data": [
        {"id": 1, "patient": "Rahul Kumar", "doctor": "Dr. Priya Sharma", "diagnosis": "Hypertension Routine Check", "date": "2026-07-22"}
    ]})

@api_bp.route('/api/prescriptions', methods=['GET'])
def api_prescriptions():
    start = time.time()
    latency = round((time.time() - start) * 1000, 2)
    return jsonify({"status": "success", "latency_ms": latency, "data": [
        {"id": 1, "patient": "Rahul Kumar", "medicine": "Paracetamol 500 mg", "dosage": "1-0-1", "days": 5}
    ]})

@api_bp.route('/api/laboratory', methods=['GET'])
def api_laboratory():
    start = time.time()
    latency = round((time.time() - start) * 1000, 2)
    return jsonify({"status": "success", "latency_ms": latency, "data": [
        {"id": 1, "patient": "Rahul Kumar", "test_name": "Complete Blood Count (CBC)", "status": "Completed", "result": "Normal"}
    ]})

@api_bp.route('/api/pharmacy', methods=['GET'])
def api_pharmacy():
    start = time.time()
    medicines = Medicine.query.all()
    result = [{"id": m.id, "code": m.medicine_code, "name": m.name, "category": m.category, "stock": m.stock, "price": m.unit_price} for m in medicines]
    latency = round((time.time() - start) * 1000, 2)
    return jsonify({"status": "success", "count": len(result), "latency_ms": latency, "data": result})

@api_bp.route('/api/billing', methods=['GET'])
def api_billing():
    start = time.time()
    bills = BillingRecord.query.all()
    result = [{"id": b.id, "bill_code": b.bill_code, "patient": b.patient_name, "amount": b.final_amount, "status": b.payment_status} for b in bills]
    latency = round((time.time() - start) * 1000, 2)
    return jsonify({"status": "success", "count": len(result), "latency_ms": latency, "data": result})

@api_bp.route('/api/notifications', methods=['GET'])
def api_notifications():
    start = time.time()
    notifs = Notification.query.all()
    result = [{"id": n.id, "code": n.notification_code, "patient": n.patient_name, "type": n.notification_type, "message": n.message, "status": n.status} for n in notifs]
    latency = round((time.time() - start) * 1000, 2)
    return jsonify({"status": "success", "count": len(result), "latency_ms": latency, "data": result})
