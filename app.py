import os
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

# Configuration
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
db_url = os.environ.get("DATABASE_URL")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
    "pool_size": 5,
    "max_overflow": 10,
    "echo": False,
}

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import models after db initialization
from models import User, Member, Page, News
from forms import LoginForm, ContactForm, MemberForm, PageForm

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Routes
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
            (Member.first_name.ilike(f'%{search}%')) |
            (Member.last_name.ilike(f'%{search}%'))
        )
    if region:
        query = query.filter_by(region=region)
        
    members = query.all()
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
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin')
@login_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

# Initialize database
with app.app_context():
    db.create_all()
    
    # Create admin user if it doesn't exist
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@cndpepci.ci', is_admin=True)
        admin.set_password('admin')  # Change this in production!
        db.session.add(admin)
        db.session.commit()
