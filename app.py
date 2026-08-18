import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from models.models import db, User, Patient, Doctor, Appointment, PatientFeedback

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ipcms-milestone1-super-secret-key-2026'

# SQLite Local Database
DB_PATH = os.path.join(os.path.dirname(__file__), "ipcms_local.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import Blueprints
from routes.auth_routes import auth_bp
from routes.patient_routes import patient_bp
from routes.doctor_routes import doctor_bp
from routes.appointment_routes import appointment_bp
from routes.dashboard_routes import dashboard_bp
from routes.textmorph_routes import textmorph_bp
from routes.pharmacy_routes import pharmacy_bp
from routes.billing_routes import billing_bp
from routes.api_routes import api_bp
from routes.notification_routes import notification_bp
from routes.analytics_routes import analytics_bp
from routes.integration_routes import integration_bp
from routes.feedback_routes import feedback_bp

app.register_blueprint(auth_bp)
app.register_blueprint(patient_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(appointment_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(textmorph_bp)
app.register_blueprint(pharmacy_bp)
app.register_blueprint(billing_bp)
app.register_blueprint(api_bp)
app.register_blueprint(notification_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(integration_bp)
app.register_blueprint(feedback_bp)


@app.route('/')
def index():
    return redirect(url_for('auth.login'))

@app.route('/portal')
def portal():
    return app.send_static_file('index.html') if os.path.exists(os.path.join(app.root_path, 'static', 'index.html')) else open(os.path.join(app.root_path, 'index.html'), encoding='utf-8').read()

@app.route('/milestone1')
@app.route('/milestone1_report.html')
def milestone1_report():
    report_path = os.path.join(app.root_path, 'milestone1_report.html')
    if os.path.exists(report_path):
        return open(report_path, encoding='utf-8').read()
    return "Milestone 1 report not found", 404

@app.route('/milestone4')
@app.route('/milestone4_report.html')
def milestone4_report():
    report_path = os.path.join(app.root_path, 'milestone4_report.html')
    if os.path.exists(report_path):
        return open(report_path, encoding='utf-8').read()
    return "Milestone 4 report not found", 404



def seed_sample_data():
    with app.app_context():
        db.create_all()

        if User.query.count() == 0:
            pw = generate_password_hash("admin123", method='scrypt')
            doc_pw = generate_password_hash("doctor123", method='scrypt')
            nurse_pw = generate_password_hash("nurse123", method='scrypt')
            pat_pw = generate_password_hash("patient123", method='scrypt')

            u1 = User(full_name="System Administrator", email="admin@ipcms.com", phone="9876543210", password=pw, role="Admin")
            u2 = User(full_name="Dr. John Smith", email="doctor@ipcms.com", phone="9876543211", password=doc_pw, role="Doctor")
            u3 = User(full_name="Sister Mary", email="nurse@ipcms.com", phone="9876543212", password=nurse_pw, role="Nurse")
            u4 = User(full_name="Rahul Kumar", email="patient@ipcms.com", phone="9876543213", password=pat_pw, role="Patient")

            db.session.add_all([u1, u2, u3, u4])
            db.session.commit()

        if Doctor.query.count() == 0:
            d1 = Doctor(doctor_code="DOC001", full_name="Dr. John Smith", specialization="Cardiologist", qualification="MD, DM (Cardio)", department="Cardiology", phone="9876543210", email="john.smith@hospital.com", available_time="10:00 AM - 02:00 PM")
            d2 = Doctor(doctor_code="DOC002", full_name="Dr. Priya Sharma", specialization="Neurologist", qualification="MD, DM (Neuro)", department="Neurology", phone="9876543211", email="priya.sharma@hospital.com", available_time="11:00 AM - 03:00 PM")
            d3 = Doctor(doctor_code="DOC003", full_name="Dr. Rahul Verma", specialization="Orthopedic", qualification="MS (Ortho)", department="Orthopedics", phone="9876543212", email="rahul.verma@hospital.com", available_time="09:00 AM - 01:00 PM")
            d4 = Doctor(doctor_code="DOC004", full_name="Dr. Anjali Mehta", specialization="Pediatrician", qualification="MD (Pedia)", department="Pediatrics", phone="9876543213", email="anjali.mehta@hospital.com", available_time="02:00 PM - 06:00 PM")
            d5 = Doctor(doctor_code="DOC005", full_name="Dr. Amit Patel", specialization="Dermatologist", qualification="MD (Dermatology)", department="Dermatology", phone="9876543214", email="amit.patel@hospital.com", available_time="10:00 AM - 04:00 PM")

            db.session.add_all([d1, d2, d3, d4, d5])
            db.session.commit()

        if Patient.query.count() == 0:
            p1 = Patient(patient_code="P001", full_name="Ravi Kumar", age=32, gender="Male", phone="9876543210", email="ravi.kumar@example.com", blood_group="O+", address="123, MG Road, Bangalore, Karnataka", medical_history="No known allergies")
            p2 = Patient(patient_code="P002", full_name="Sneha Sharma", age=28, gender="Female", phone="9123456780", email="sneha.s@example.com", blood_group="A+", address="45, Park Street, Kolkata", medical_history="Asthma")
            p3 = Patient(patient_code="P003", full_name="Arjun Patel", age=45, gender="Male", phone="9988776655", email="arjun.p@example.com", blood_group="B+", address="88, SG Highway, Ahmedabad", medical_history="Hypertension")
            p4 = Patient(patient_code="P004", full_name="Priya Nair", age=31, gender="Female", phone="8899001122", email="priya.n@example.com", blood_group="AB+", address="12, Marine Drive, Mumbai", medical_history="None")
            p5 = Patient(patient_code="P005", full_name="Vikram Singh", age=38, gender="Male", phone="7766554433", email="vikram.s@example.com", blood_group="O-", address="67, Ring Road, Delhi", medical_history="Type 2 Diabetes")

            db.session.add_all([p1, p2, p3, p4, p5])
            db.session.commit()

        if Appointment.query.count() == 0:
            a1 = Appointment(appointment_code="APT001", patient_id=1, patient_name="Ravi Kumar", doctor_id=1, doctor_name="Dr. John Smith (Cardiologist)", appointment_date="2026-05-20", appointment_time="10:30 AM", status="Confirmed")
            a2 = Appointment(appointment_code="APT002", patient_id=2, patient_name="Sneha Sharma", doctor_id=2, doctor_name="Dr. Priya Sharma (Neurologist)", appointment_date="2026-05-20", appointment_time="11:30 AM", status="Scheduled")
            a3 = Appointment(appointment_code="APT003", patient_id=3, patient_name="Arjun Patel", doctor_id=3, doctor_name="Dr. Rahul Verma (Orthopedic)", appointment_date="2026-05-20", appointment_time="12:30 PM", status="Scheduled")
            db.session.add_all([a1, a2, a3])
            db.session.commit()

        if PatientFeedback.query.count() == 0:
            f1 = PatientFeedback(patient_id=1, patient_name="Ravi Kumar", doctor_id=1, doctor_name="Dr. John Smith", department="Cardiology", doctor_rating=5, hospital_rating=5, lab_rating=4, pharmacy_rating=5, comments="Excellent consultation and care by Dr. Smith. Very attentive and professional.")
            f2 = PatientFeedback(patient_id=2, patient_name="Sneha Sharma", doctor_id=2, doctor_name="Dr. Priya Sharma", department="Neurology", doctor_rating=5, hospital_rating=4, lab_rating=5, pharmacy_rating=4, comments="Dr. Priya explained the diagnosis thoroughly. Lab test reports were delivered quickly.")
            f3 = PatientFeedback(patient_id=3, patient_name="Arjun Patel", doctor_id=3, doctor_name="Dr. Rahul Verma", department="Orthopedics", doctor_rating=4, hospital_rating=4, lab_rating=4, pharmacy_rating=4, comments="Good experience overall. Pharmacy wait time could be slightly shorter.")
            db.session.add_all([f1, f2, f3])
            db.session.commit()




seed_sample_data()

if __name__ == '__main__':
    app.run(debug=True, port=5000)

