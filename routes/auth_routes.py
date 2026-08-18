from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        user_role = request.form.get('role')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f'Welcome back, {user.full_name} ({user.role})!', 'success')

            # Open corresponding view page for the logged in role
            if user.role == 'Doctor':
                return redirect(url_for('doctor.list_doctors'))
            elif user.role == 'Nurse':
                return redirect(url_for('patient.list_patients'))
            elif user.role == 'Patient':
                return redirect(url_for('appointment.list_appointments'))
            else:
                return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Incorrect email or password! Please check your credentials and try again.', 'danger')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        role = request.form.get('role', 'Patient')

        existing = User.query.filter_by(email=email).first()
        if existing:
            flash('Email already registered! Please log in.', 'warning')
            return redirect(url_for('auth.login'))

        hashed_pw = generate_password_hash(password, method='scrypt')
        new_user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            password=hashed_pw,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login with your credentials.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out safely.', 'info')
    return redirect(url_for('auth.login'))
