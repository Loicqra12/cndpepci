from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime
import os
from PIL import Image

from models import db, User, Member, Page, News
from forms import LoginForm, MemberForm, PageForm

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Accès non autorisé.', 'error')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

def optimize_image(image_path, max_size=(800, 800)):
    with Image.open(image_path) as img:
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        img.save(image_path, optimize=True, quality=85)

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        flash('Nom d\'utilisateur ou mot de passe invalide', 'error')
    return render_template('admin/login.html', form=form)

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@admin.route('/')
@admin.route('/dashboard')
@admin_required
def dashboard():
    total_members = Member.query.count()
    active_members = Member.query.filter_by(active=True).count()
    total_pages = Page.query.count()
    total_news = News.query.count()
    recent_members = Member.query.order_by(Member.id.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_members=total_members,
                         active_members=active_members,
                         total_pages=total_pages,
                         total_news=total_news,
                         recent_members=recent_members)

@admin.route('/members')
@admin_required
def members():
    members = Member.query.all()
    form = MemberForm()
    return render_template('admin/members.html', members=members, form=form)

@admin.route('/members/add', methods=['POST'])
@admin_required
def add_member():
    form = MemberForm()
    if form.validate_on_submit():
        member = Member()
        form.populate_obj(member)
        
        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            form.photo.data.save(photo_path)
            optimize_image(photo_path)
            member.photo_url = os.path.join('images/members', filename)
            
        db.session.add(member)
        db.session.commit()
        flash('Nouveau membre ajouté avec succès.', 'success')
        return redirect(url_for('admin.members'))
        
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{getattr(form, field).label.text}: {error}', 'error')
    return redirect(url_for('admin.members'))

@admin.route('/members/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def member_edit(id):
    member = Member.query.get_or_404(id)
    form = MemberForm(obj=member)
    
    if form.validate_on_submit():
        form.populate_obj(member)
        
        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            form.photo.data.save(photo_path)
            optimize_image(photo_path)
            member.photo_url = os.path.join('images/members', filename)
            
        db.session.commit()
        flash('Membre mis à jour avec succès.', 'success')
        return redirect(url_for('admin.members'))
        
    return render_template('admin/member_edit.html', form=form, member=member)

@admin.route('/members/<int:id>')
@admin_required
def member_details(id):
    member = Member.query.get_or_404(id)
    return render_template('admin/member_details.html', member=member)

@admin.route('/content')
@admin_required
def content():
    pages = Page.query.all()
    news = News.query.order_by(News.date_posted.desc()).all()
    form = PageForm()
    return render_template('admin/content.html', pages=pages, news=news, form=form)
