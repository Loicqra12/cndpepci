import os
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images', 'members')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
app.config['SESSION_TYPE'] = 'filesystem'

# Sécurité
Talisman(app, content_security_policy={
    'default-src': "'self'",
    'img-src': "'self' data: https:",
    'script-src': "'self' 'unsafe-inline' 'unsafe-eval' https://cdnjs.cloudflare.com",
    'style-src': "'self' 'unsafe-inline' https://cdnjs.cloudflare.com",
    'font-src': "'self' https://cdnjs.cloudflare.com"
})

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

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

# Register blueprints
from blueprints.admin import admin
app.register_blueprint(admin)

# Error handlers
@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(f'Page not found: {request.url}')
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error(f'Server Error: {error}')
    return render_template('errors/500.html'), 500

# Configure logging
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    import os
    
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/cndpepci.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('CNDPEPCI startup')
# Initialize database
with app.app_context():
    db.create_all()
    
    # Create admin user if it doesn't exist
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@cndpepci.ci', is_admin=True)
        admin.set_password('admin')  # Change this in production!
        db.session.add(admin)
        db.session.commit()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)