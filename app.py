import os
from flask import Flask, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user, login_user, logout_user, LoginManager
from werkzeug.utils import secure_filename
from extensions import db, login_manager, migrate
from flask_wtf.csrf import CSRFProtect

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cndpepci.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images', 'members')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf = CSRFProtect(app)

    with app.app_context():
        # Import models
        from models import User, Member, Page, News

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # Register blueprints
        from blueprints import init_app
        init_app(app)

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
            bureau = [
                {
                    'name': 'KOUASSI Yao',
                    'role': 'Président',
                    'description': 'Détective privé expérimenté et fondateur de la CNDPEPCI',
                    'photo': url_for('static', filename='images/members/kouassi_yao.jpg')
                },
                {
                    'name': 'LAGO Hugues',
                    'role': 'Vice-Président',
                    'description': 'Expert en investigation et formation professionnelle',
                    'photo': url_for('static', filename='images/members/hugues_lago.jpg')
                },
                {
                    'name': 'DIABY Adams',
                    'role': 'Secrétaire Général',
                    'description': 'Spécialiste en réglementation et affaires juridiques',
                    'photo': url_for('static', filename='images/members/adams_diaby.jpg')
                }
            ]
            
            commissions = [
                {
                    'name': 'Commission Formation et Certification',
                    'president': 'HONDE Jean-Michel',
                    'description': 'Responsable des programmes de formation et de la certification des détectives',
                    'members': ['HONDE Jean-Michel', 'OUA Bernard', 'MBO Abraham']
                },
                {
                    'name': 'Commission Éthique et Déontologie',
                    'president': 'BALLIET Fernand',
                    'description': 'Veille au respect des règles déontologiques de la profession',
                    'members': ['BALLIET Fernand', 'LAGO Hugues', 'DIABY Adams']
                }
            ]
            
            return render_template('equipe.html', bureau=bureau, commissions=commissions)

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
            
            # Préparer les données pour l'affichage
            for member in members:
                member.domains_list = member.get_domains_list()
                member.certifications_list = member.get_certifications_list()
                
            return render_template('directory.html', members=members)

        @app.route('/annuaire')
        def annuaire():
            members = Member.query.filter_by(active=True).all()
            return render_template('annuaire.html', members=members)

        @app.route('/contact', methods=['GET', 'POST'])
        def contact():
            from forms import ContactForm
            form = ContactForm()
            if form.validate_on_submit():
                # Here you would typically send an email
                flash('Message envoyé avec succès!', 'success')
                return redirect(url_for('contact'))
            return render_template('contact.html', form=form)

        # Dashboard login route
        @app.route('/dashboard/login', methods=['GET', 'POST'])
        def dashboard_login():
            from forms import LoginForm
            if current_user.is_authenticated:
                return redirect(url_for('dashboard_home'))
            
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
                    return redirect(url_for('dashboard_home'))
            return render_template('admin/login.html', form=form)

        @app.route('/dashboard/logout')
        @login_required
        def dashboard_logout():
            logout_user()
            return redirect(url_for('dashboard_login'))

        @app.route('/dashboard')
        @app.route('/dashboard/home')
        @login_required
        def dashboard_home():
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

        @app.route('/dashboard/members')
        @login_required
        def dashboard_members():
            from forms import MemberForm
            members = Member.query.all()
            form = MemberForm()
            return render_template('admin/members.html', members=members, form=form)

        @app.route('/dashboard/content')
        @login_required
        def dashboard_content():
            from forms import PageForm, NewsForm
            pages = Page.query.all()
            news = News.query.all()
            form = PageForm()
            news_form = NewsForm()
            return render_template('admin/content.html', pages=pages, news=news, form=form, news_form=news_form)

        @app.route('/dashboard/members/add', methods=['POST'])
        @login_required
        def dashboard_add_member():
            from forms import MemberForm
            form = MemberForm()
            if form.validate_on_submit():
                try:
                    member = Member()
                    # Copier les champs du formulaire vers l'objet member
                    member.first_name = form.first_name.data
                    member.last_name = form.last_name.data
                    member.email = form.email.data
                    member.phone = form.phone.data
                    member.region = form.region.data
                    member.specialization = form.specialization.data
                    member.bio = form.bio.data
                    member.address = form.address.data
                    member.agency_name = form.agency_name.data
                    member.role = form.role.data
                    member.license_number = form.license_number.data
                    member.experience_years = form.experience_years.data
                    member.website = form.website.data
                    member.active = form.active.data if form.active.data is not None else True
                    member.latitude = form.latitude.data
                    member.longitude = form.longitude.data
                    
                    # Gestion de la photo
                    if form.photo.data:
                        filename = secure_filename(form.photo.data.filename)
                        photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                        form.photo.data.save(photo_path)
                        member.photo_url = filename

                    # Gestion des domaines et certifications
                    member.domains = form.domains.data
                    member.certifications = form.certifications.data
                    
                    db.session.add(member)
                    db.session.commit()
                    flash('Membre ajouté avec succès.', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash(f'Erreur lors de l\'ajout du membre: {str(e)}', 'error')
                return redirect(url_for('dashboard_members'))
            
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{getattr(form, field).label.text}: {error}', 'error')
            return redirect(url_for('dashboard_members'))

        @app.route('/dashboard/members/edit/<int:id>', methods=['GET', 'POST'])
        @login_required
        def dashboard_member_edit(id):
            member = Member.query.get_or_404(id)
            from forms import MemberForm
            
            if request.method == 'GET':
                # Convertir les domaines et certifications en format lisible
                if member.domains:
                    member.domains = '\n'.join(member.domains.split(','))
                if member.certifications:
                    member.certifications = '\n'.join(member.certifications.split(','))
            
            form = MemberForm(obj=member)
            
            if form.validate_on_submit():
                form.populate_obj(member)
                
                # Gestion de la photo
                if form.photo.data:
                    filename = secure_filename(form.photo.data.filename)
                    photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    form.photo.data.save(photo_path)
                    member.photo_url = filename

                # Gestion des domaines et certifications
                if form.domains.data:
                    member.domains = ','.join(form.domains.data.split('\n'))
                if form.certifications.data:
                    member.certifications = ','.join(form.certifications.data.split('\n'))
                    
                db.session.commit()
                flash('Membre mis à jour avec succès.', 'success')
                return redirect(url_for('dashboard_members'))
                
            return render_template('admin/member_edit.html', form=form, member=member)

        @app.route('/dashboard/members/delete/<int:id>', methods=['POST'])
        @login_required
        def dashboard_member_delete(id):
            member = Member.query.get_or_404(id)
            db.session.delete(member)
            db.session.commit()
            flash('Membre supprimé avec succès.', 'success')
            return redirect(url_for('dashboard_members'))

        @app.route('/dashboard/members/toggle/<int:id>', methods=['POST'])
        @login_required
        def dashboard_member_toggle(id):
            member = Member.query.get_or_404(id)
            member.active = not member.active
            db.session.commit()
            status = "activé" if member.active else "désactivé"
            flash(f'Membre {status} avec succès.', 'success')
            return redirect(url_for('dashboard_members'))

        @app.route('/admin/members/<int:id>')
        @login_required
        def admin_member_details(id):
            member = Member.query.get_or_404(id)
            return render_template('admin/member_details.html', member=member)

        @app.route('/dashboard/content/add-page', methods=['POST'])
        @login_required
        def dashboard_add_page():
            from forms import PageForm
            form = PageForm()
            if form.validate_on_submit():
                try:
                    page = Page()
                    page.title = form.title.data
                    page.slug = form.slug.data
                    page.content = form.content.data
                    db.session.add(page)
                    db.session.commit()
                    flash('Page ajoutée avec succès.', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash(f'Erreur lors de l\'ajout de la page: {str(e)}', 'error')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        flash(f'{getattr(form, field).label.text}: {error}', 'error')
            return redirect(url_for('dashboard_content'))

        @app.route('/dashboard/content/add-news', methods=['POST'])
        @login_required
        def dashboard_add_news():
            from forms import NewsForm
            form = NewsForm()
            if form.validate_on_submit():
                try:
                    news = News()
                    news.title = form.title.data
                    news.content = form.content.data
                    news.type = form.type.data
                    
                    # Gestion de l'image
                    if form.image.data:
                        filename = secure_filename(form.image.data.filename)
                        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'news', filename)
                        os.makedirs(os.path.dirname(image_path), exist_ok=True)
                        form.image.data.save(image_path)
                        news.image_url = filename

                    db.session.add(news)
                    db.session.commit()
                    flash('Actualité ajoutée avec succès.', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash(f'Erreur lors de l\'ajout de l\'actualité: {str(e)}', 'error')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        flash(f'{getattr(form, field).label.text}: {error}', 'error')
            return redirect(url_for('dashboard_content'))

        @app.route('/dashboard/content/edit-page/<int:id>', methods=['GET', 'POST'])
        @login_required
        def dashboard_edit_page(id):
            page = Page.query.get_or_404(id)
            form = PageForm(obj=page)
            
            if form.validate_on_submit():
                try:
                    page.title = form.title.data
                    page.slug = form.slug.data
                    page.content = form.content.data
                    db.session.commit()
                    flash('Page modifiée avec succès.', 'success')
                    return redirect(url_for('dashboard_content'))
                except Exception as e:
                    db.session.rollback()
                    flash(f'Erreur lors de la modification de la page: {str(e)}', 'error')
            
            return render_template('admin/edit_page.html', form=form, page=page)

        @app.route('/dashboard/content/delete-page/<int:id>', methods=['POST'])
        @login_required
        def dashboard_delete_page(id):
            page = Page.query.get_or_404(id)
            try:
                db.session.delete(page)
                db.session.commit()
                flash('Page supprimée avec succès.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Erreur lors de la suppression de la page: {str(e)}', 'error')
            return redirect(url_for('dashboard_content'))

        @app.route('/dashboard/content/edit-news/<int:id>', methods=['GET', 'POST'])
        @login_required
        def dashboard_edit_news(id):
            news = News.query.get_or_404(id)
            form = NewsForm(obj=news)
            
            if form.validate_on_submit():
                try:
                    news.title = form.title.data
                    news.content = form.content.data
                    news.type = form.type.data
                    
                    if form.image.data:
                        # Supprimer l'ancienne image si elle existe
                        if news.image_url:
                            old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'news', news.image_url)
                            if os.path.exists(old_image_path):
                                os.remove(old_image_path)
                        
                        # Sauvegarder la nouvelle image
                        filename = secure_filename(form.image.data.filename)
                        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'news', filename)
                        os.makedirs(os.path.dirname(image_path), exist_ok=True)
                        form.image.data.save(image_path)
                        news.image_url = filename
                    
                    db.session.commit()
                    flash('Actualité modifiée avec succès.', 'success')
                    return redirect(url_for('dashboard_content'))
                except Exception as e:
                    db.session.rollback()
                    flash(f'Erreur lors de la modification de l\'actualité: {str(e)}', 'error')
            
            return render_template('admin/edit_news.html', form=form, news=news)

        @app.route('/dashboard/content/delete-news/<int:id>', methods=['POST'])
        @login_required
        def dashboard_delete_news(id):
            news = News.query.get_or_404(id)
            try:
                # Supprimer l'image associée si elle existe
                if news.image_url:
                    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'news', news.image_url)
                    if os.path.exists(image_path):
                        os.remove(image_path)
                
                db.session.delete(news)
                db.session.commit()
                flash('Actualité supprimée avec succès.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Erreur lors de la suppression de l\'actualité: {str(e)}', 'error')
            return redirect(url_for('dashboard_content'))

        # Create database tables
        db.create_all()

        # Create admin user if it doesn't exist
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@cndpepci.ci', is_admin=True)
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)