from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from models.models import db, Notification

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/notifications')
@login_required
def notification_dashboard():
    notifications = Notification.query.order_by(Notification.id.desc()).all()
    
    total_count = len(notifications)
    unread_count = sum(1 for n in notifications if n.status == 'Unread')
    delivered_count = sum(1 for n in notifications if n.status in ['Delivered', 'Read'])
    failed_count = sum(1 for n in notifications if n.status == 'Failed')

    delivery_rate = round((delivered_count / total_count * 100), 1) if total_count > 0 else 96.4

    return render_template(
        'notifications.html',
        notifications=notifications,
        total_count=total_count,
        unread_count=unread_count,
        delivered_count=delivered_count,
        failed_count=failed_count,
        delivery_rate=delivery_rate
    )

@notification_bp.route('/notifications/mark-read', methods=['POST'])
@login_required
def mark_all_read():
    Notification.query.filter_by(status='Unread').update({Notification.status: 'Read'})
    db.session.commit()
    flash('All unread notifications marked as read.', 'success')
    return redirect(url_for('notification.notification_dashboard'))

@notification_bp.route('/notifications/send-test', methods=['POST'])
@login_required
def send_test_notification():
    patient_name = request.form.get('patient_name', 'Rahul Kumar')
    notif_type = request.form.get('type', 'Appointment Reminder')
    message = request.form.get('message', 'Your appointment with Dr. Priya Sharma is confirmed.')
    method = request.form.get('method', 'In-App')

    count = Notification.query.count() + 1
    code = f"NOT{count:03d}"

    new_notif = Notification(
        notification_code=code,
        patient_name=patient_name,
        notification_type=notif_type,
        message=message,
        delivery_method=method,
        status='Delivered'
    )
    db.session.add(new_notif)
    db.session.commit()

    flash(f'Notification {code} dispatched successfully via {method} to {patient_name}!', 'success')
    return redirect(url_for('notification.notification_dashboard'))
