from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from extensions import db
from models import User
from datetime import datetime, timedelta

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_home'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False) == 'on'
        
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            flash('Nom d\'utilisateur inconnu', 'error')
        elif not user.check_password(password):
            flash('Mot de passe incorrect', 'error')
        else:
            login_user(user, remember=remember)
            user.last_seen = datetime.utcnow()
            db.session.commit()
            flash('Connexion réussie!', 'success')
            
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('dashboard_home')
            return redirect(next_page)
            
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_home'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            user.generate_reset_token()
            # Ici vous devriez envoyer un email avec le lien de réinitialisation
            flash('Un email avec les instructions pour réinitialiser votre mot de passe vous a été envoyé.', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash('Adresse email inconnue.', 'error')
            
    return render_template('auth/reset_password_request.html')

@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_home'))
        
    user = User.query.filter_by(reset_password_token=token).first()
    
    if not user or user.reset_password_expires < datetime.utcnow():
        flash('Le lien de réinitialisation est invalide ou a expiré.', 'error')
        return redirect(url_for('auth.reset_password_request'))
        
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'error')
        else:
            user.set_password(password)
            user.reset_password_token = None
            user.reset_password_expires = None
            db.session.commit()
            flash('Votre mot de passe a été réinitialisé.', 'success')
            return redirect(url_for('auth.login'))
            
    return render_template('auth/reset_password.html')
