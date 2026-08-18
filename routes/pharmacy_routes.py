from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from models.models import db, Medicine

pharmacy_bp = Blueprint('pharmacy', __name__)

@pharmacy_bp.route('/pharmacy')
@login_required
def pharmacy_dashboard():
    medicines = Medicine.query.order_by(Medicine.id.asc()).all()
    total_medicines = Medicine.query.count()
    available_stock = sum(m.stock for m in medicines)
    low_stock_count = sum(1 for m in medicines if m.stock <= 50 and m.stock > 0)
    expired_count = sum(1 for m in medicines if m.status == 'Expired')
    dispensed_today = 36 # Sample KPI metric

    return render_template(
        'pharmacy.html',
        medicines=medicines,
        total_medicines=total_medicines,
        available_stock=available_stock,
        low_stock_count=low_stock_count,
        expired_count=expired_count,
        dispensed_today=dispensed_today
    )

@pharmacy_bp.route('/pharmacy/add', methods=['POST'])
@login_required
def add_medicine():
    name = request.form.get('name', '').strip()
    category = request.form.get('category', 'Tablet').strip()
    manufacturer = request.form.get('manufacturer', '').strip()
    stock = int(request.form.get('stock', 0))
    unit_price = float(request.form.get('unit_price', 0.0))
    expiry_date = request.form.get('expiry_date', '').strip()

    count = Medicine.query.count() + 1
    medicine_code = f"MED{count:03d}"
    status = 'Available' if stock > 50 else ('Low Stock' if stock > 0 else 'Expired')

    new_med = Medicine(
        medicine_code=medicine_code,
        name=name,
        category=category,
        manufacturer=manufacturer,
        stock=stock,
        unit_price=unit_price,
        expiry_date=expiry_date,
        status=status
    )
    db.session.add(new_med)
    db.session.commit()

    flash(f'Medicine {name} added to inventory ({medicine_code})', 'success')
    return redirect(url_for('pharmacy.pharmacy_dashboard'))

@pharmacy_bp.route('/pharmacy/dispense', methods=['POST'])
@login_required
def dispense_medicine():
    medicine_id = request.form.get('medicine_id', type=int)
    qty = request.form.get('quantity', type=int, default=1)

    med = Medicine.query.get_or_404(medicine_id)
    if med.stock >= qty:
        med.stock -= qty
        if med.stock <= 50 and med.stock > 0:
            med.status = 'Low Stock'
        elif med.stock == 0:
            med.status = 'Expired'
        db.session.commit()
        flash(f'Successfully dispensed {qty} units of {med.name}. Remaining stock: {med.stock}', 'success')
    else:
        flash(f'Insufficient stock for {med.name}. Available: {med.stock}', 'danger')

    return redirect(url_for('pharmacy.pharmacy_dashboard'))
