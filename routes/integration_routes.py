from flask import Blueprint, render_template
from flask_login import login_required

integration_bp = Blueprint('integration', __name__)

@integration_bp.route('/system-integration')
@login_required
def integration_dashboard():
    modules = [
        {"name": "Patient Management", "status": "Connected", "last_sync": "23-07-2026 11:25 AM"},
        {"name": "Appointment Management", "status": "Connected", "last_sync": "23-07-2026 11:25 AM"},
        {"name": "EHR Management", "status": "Connected", "last_sync": "23-07-2026 11:24 AM"},
        {"name": "Consultation Management", "status": "Connected", "last_sync": "23-07-2026 11:24 AM"},
        {"name": "Prescription Management", "status": "Connected", "last_sync": "23-07-2026 11:23 AM"},
        {"name": "Laboratory Management", "status": "Connected", "last_sync": "23-07-2026 11:23 AM"},
        {"name": "Pharmacy Management", "status": "Connected", "last_sync": "23-07-2026 11:22 AM"},
        {"name": "Billing & Payment", "status": "Connected", "last_sync": "23-07-2026 11:22 AM"},
        {"name": "Notification Management", "status": "Connected", "last_sync": "23-07-2026 11:21 AM"},
        {"name": "Dashboard Analytics", "status": "Connected", "last_sync": "23-07-2026 11:21 AM"}
    ]

    test_results = [
        {"test": "Module Communication", "status": "Passed", "details": "All modules communicating correctly", "tested_on": "23-07-2026 10:30 AM"},
        {"test": "Database Connectivity", "status": "Passed", "details": "Database connected and synced", "tested_on": "23-07-2026 10:28 AM"},
        {"test": "API Integration", "status": "Passed", "details": "All APIs responding correctly (< 300 ms)", "tested_on": "23-07-2026 10:25 AM"},
        {"test": "Notification Delivery", "status": "Passed", "details": "Notifications sent successfully (98% rate)", "tested_on": "23-07-2026 10:20 AM"},
        {"test": "Data Consistency", "status": "Passed", "details": "All data consistent across modules", "tested_on": "23-07-2026 10:15 AM"},
        {"test": "Security Testing", "status": "Passed", "details": "Authentication & authorization working", "tested_on": "23-07-2026 10:10 AM"}
    ]

    return render_template(
        'integration.html',
        modules=modules,
        test_results=test_results
    )
