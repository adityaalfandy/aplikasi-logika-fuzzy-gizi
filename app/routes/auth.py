from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, RegisterForm
from app.models.user import User
from app import db, bcrypt

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(nama=form.nama.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Akun Anda telah dibuat! Silakan login.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login berhasil!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Gagal. Silakan periksa email dan password Anda.', 'error')
            
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('Anda telah berhasil logout.', 'info')
    return redirect(url_for('main.index'))

from app.forms import UpdateProfileForm

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        # Update email and name
        current_user.nama = form.nama.data
        current_user.email = form.email.data
        
        # Update password if old password matches and new password is provided
        if form.new_password.data:
            if not form.old_password.data:
                flash('Masukkan password saat ini untuk mengubah password baru.', 'danger')
                return render_template('auth/profile.html', form=form)
            
            if not bcrypt.check_password_hash(current_user.password_hash, form.old_password.data):
                flash('Password saat ini salah.', 'danger')
                return render_template('auth/profile.html', form=form)
                
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password_hash = hashed_password
            
        db.session.commit()
        flash('Profil berhasil diperbarui!', 'success')
        return redirect(url_for('auth.profile'))
        
    elif request.method == 'GET':
        form.nama.data = current_user.nama
        form.email.data = current_user.email
        
    return render_template('auth/profile.html', form=form)
