import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images', 'members')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
import os
import shutil

def add_member_with_photo(member_data, photo_filename, source_photo_path):
    """
    Ajoute un nouveau membre avec sa photo
    """
    # Créer le dossier des photos si nécessaire
    upload_folder = os.path.join('static', 'images', 'members')
    os.makedirs(upload_folder, exist_ok=True)
    
    # Copier la photo
    destination = os.path.join(upload_folder, photo_filename)
    shutil.copy2(source_photo_path, destination)
    
    # Créer le membre
    member = Member(**member_data)
    member.photo_url = photo_filename
    member.active = True
    
    # Sauvegarder dans la base de données
    db.session.add(member)
    db.session.commit()
    
    return member

# Import models after db initialization
from models import User, Member, Page, News
from forms import LoginForm, ContactForm, MemberForm, PageForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    news = News.query.order_by(News.date_posted.desc()).limit(3).all()
    return render_template('home.html', news=news)

@app.route('/about')
def about():
    page = Page.query.filter_by(slug='about').first()
    return render_template('about.html', page=page)

@app.route('/profession/metier')
def profession_metier():
    return render_template('profession/metier.html')

@app.route('/profession/reglementation')
def profession_reglementation():
    return render_template('profession/reglementation.html')

@app.route('/profession/activite')
def profession_activite():
    return render_template('profession/activite.html')

@app.route('/client/services')
def client_services():
    return render_template('client/services.html')

@app.route('/client/faq')
def client_faq():
    return render_template('client/faq.html')

@app.route('/formation/programmes')
def formation_programmes():
    return render_template('formation/programmes.html')

@app.route('/formation/certification')
def formation_certification():
    return render_template('formation/certification.html')

@app.route('/formation/calendrier')
def formation_calendrier():
    return render_template('formation/calendrier.html')

@app.route('/presse/actualites')
def presse_actualites():
    articles = News.query.order_by(News.date_posted.desc()).all()
    return render_template('presse/actualites.html', articles=articles)

@app.route('/presse/communiques')
def presse_communiques():
    communiques = News.query.filter_by(type='communique').order_by(News.date_posted.desc()).all()
    return render_template('presse/communiques.html', communiques=communiques)

@app.route('/presse/medias')
def presse_medias():
    return render_template('presse/medias.html')

@app.route('/equipe')
def equipe():
    return render_template('equipe.html')

@app.route('/president')
def president():
    page = Page.query.filter_by(slug='president').first()
    return render_template('president.html', page=page)

@app.route('/deontology')
def deontology():
    page = Page.query.filter_by(slug='deontology').first()
    return render_template('deontology.html', page=page)

@app.route('/activities')
def activities():
    page = Page.query.filter_by(slug='activities').first()
    return render_template('activities.html', page=page)

@app.route('/directory')
def directory():
    search = request.args.get('search', '')
    region = request.args.get('region', '')
    
    query = Member.query.filter_by(active=True)
    
    if search:
        query = query.filter(
            db.or_(
                Member.first_name.ilike(f'%{search}%'),
                Member.last_name.ilike(f'%{search}%'),
                Member.agency_name.ilike(f'%{search}%'),
                Member.specialization.ilike(f'%{search}%')
            )
        )
    if region:
        query = query.filter_by(region=region)
        
    members = query.all()
    
    # Convert domains and certifications from string to list
    for member in members:
        if member.domains:
            member.domains = member.domains.split(',')
        else:
            member.domains = []
            
        if member.certifications:
            member.certifications = member.certifications.split(',')
        else:
            member.certifications = []
    return render_template('directory.html', members=members)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Here you would typically send an email
        flash('Message envoyé avec succès!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('Nom d\'utilisateur inconnu', 'error')
        elif not user.check_password(form.password.data):
            flash('Mot de passe incorrect', 'error')
        else:
            login_user(user)
            flash('Connexion réussie!', 'success')
            return redirect(url_for('admin_dashboard'))
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin')
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    total_members = Member.query.count()
    active_members = Member.query.filter_by(active=True).count()
    total_pages = Page.query.count()
    total_news = News.query.count()
    
    # Récupérer les derniers membres ajoutés
    recent_members = Member.query.order_by(Member.id.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_members=total_members,
                         active_members=active_members,
                         total_pages=total_pages,
                         total_news=total_news,
                         recent_members=recent_members)

@app.route('/admin/members')
@login_required
def admin_members():
    members = Member.query.all()
    form = MemberForm()
    return render_template('admin/members.html', members=members, form=form)

@app.route('/admin/members/add', methods=['POST'])
@login_required
def admin_add_member():
    form = MemberForm()
    if form.validate_on_submit():
        member = Member()
        form.populate_obj(member)
        
        # Gestion de la photo
        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.photo.data.save(photo_path)
            member.photo_url = filename
            
        db.session.add(member)
        db.session.commit()
        flash('Nouveau membre ajouté avec succès.', 'success')
        return redirect(url_for('admin_members'))
        
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{getattr(form, field).label.text}: {error}', 'error')
    return redirect(url_for('admin_members'))

@app.route('/admin/members/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_member_edit(id):
    member = Member.query.get_or_404(id)
    form = MemberForm(obj=member)
    
    if form.validate_on_submit():
        form.populate_obj(member)
        
        # Gestion de la photo
        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.photo.data.save(photo_path)
            member.photo_url = filename
            
        db.session.commit()
        flash('Membre mis à jour avec succès.', 'success')
        return redirect(url_for('admin_members'))
        
    return render_template('admin/member_edit.html', form=form, member=member)

@app.route('/admin/members/<int:id>')
@login_required
def admin_member_details(id):
    member = Member.query.get_or_404(id)
    return render_template('admin/member_details.html', member=member)

@app.route('/admin/content')
@login_required
def admin_content():
    pages = Page.query.all()
    news = News.query.order_by(News.date_posted.desc()).all()
    form = PageForm()
    return render_template('admin/content.html', pages=pages, news=news, form=form)

# Initialize database
with app.app_context():
    db.create_all()
    
    # Create admin user if it doesn't exist
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@cndpepci.ci', is_admin=True)
        admin.set_password('admin')  # Change this in production!
        db.session.add(admin)
        db.session.commit()