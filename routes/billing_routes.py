from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.models import db, Patient, BillingRecord, BillingItem
import uuid

billing_bp = Blueprint('billing', __name__)

@billing_bp.route('/billing', methods=['GET'])
@login_required
def billing_page():
    patient_id_query = request.args.get('patient_id', 'P001').strip()
    patient = Patient.query.filter((Patient.patient_code == patient_id_query) | (Patient.full_name.ilike(f'%{patient_id_query}%'))).first()
    
    if not patient:
        patient = Patient.query.first()

    # Retrieve existing billing records or construct sample items
    billing_history = BillingRecord.query.order_by(BillingRecord.id.desc()).all()

    sample_items = [
        {"type": "Consultation", "desc": "Dr. Priya - General Medicine", "ref": "CONS1001", "date": "22-07-2026", "amount": 500.00},
        {"type": "Laboratory", "desc": "Complete Blood Count (CBC)", "ref": "LAB1001", "date": "22-07-2026", "amount": 550.00},
        {"type": "Laboratory", "desc": "Lipid Profile", "ref": "LAB1002", "date": "22-07-2026", "amount": 300.00},
        {"type": "Pharmacy", "desc": "Paracetamol 500 mg (10 Tablets)", "ref": "PHAR1001", "date": "22-07-2026", "amount": 150.00},
        {"type": "Pharmacy", "desc": "Amoxicillin 250 mg (10 Capsules)", "ref": "PHAR1002", "date": "22-07-2026", "amount": 300.00},
        {"type": "Other Charges", "desc": "Registration Charges", "ref": "OTH1001", "date": "22-07-2026", "amount": 200.00}
    ]

    total_amount = sum(item["amount"] for item in sample_items)

    return render_template(
        'billing.html',
        patient=patient,
        items=sample_items,
        total_amount=total_amount,
        billing_history=billing_history
    )

@billing_bp.route('/billing/pay', methods=['POST'])
@login_required
def process_payment():
    patient_id = request.form.get('patient_id', type=int)
    patient_name = request.form.get('patient_name', 'Rahul Kumar')
    amount = float(request.form.get('amount', 2000.00))
    payment_method = request.form.get('payment_method', 'UPI')

    count = BillingRecord.query.count() + 1
    bill_code = f"BILL{count:03d}"
    txn_id = f"UPI{uuid.uuid4().hex[:10].upper()}"

    new_bill = BillingRecord(
        bill_code=bill_code,
        patient_id=patient_id if patient_id else 1,
        patient_name=patient_name,
        total_amount=amount,
        discount=0.0,
        tax=0.0,
        final_amount=amount,
        payment_method=payment_method,
        transaction_id=txn_id,
        payment_status='Paid'
    )
    db.session.add(new_bill)
    db.session.commit()

    flash(f'Payment of ₹{amount:,.2f} recorded successfully for {patient_name}! Invoice {bill_code} generated.', 'success')
    return redirect(url_for('billing.billing_page'))
