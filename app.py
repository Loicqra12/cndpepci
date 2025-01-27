import os
import psycopg2
from flask import Flask, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user, login_user, logout_user, LoginManager
from werkzeug.utils import secure_filename
from extensions import db, login_manager, migrate
from flask_wtf.csrf import CSRFProtect
from models import User, Member, ForumTopic, ForumPost, ForumCategory, Page, News
from error import configure_error_handlers
from config import Config
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration depuis la classe Config
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf = CSRFProtect(app)

    # Configure Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = 'admin_login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    login_manager.login_message_category = 'info'

    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    def add_member_with_photo(member_data, photo_filename=None, source_photo_path=None):
        try:
            # Créer une nouvelle instance de Member avec les données fournies
            new_member = Member(**member_data)
            
            # Si une photo est fournie, la copier dans le dossier des uploads
            if photo_filename and source_photo_path:
                if os.path.exists(source_photo_path):
                    target_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
                    import shutil
                    shutil.copy2(source_photo_path, target_path)
                    new_member.photo_url = photo_filename
            
            # Ajouter et sauvegarder le membre dans la base de données
            db.session.add(new_member)
            db.session.commit()
            print(f"Membre {new_member.first_name} {new_member.last_name} ajouté avec succès!")
            return new_member
        except Exception as e:
            print(f"Erreur lors de l'ajout du membre: {str(e)}")
            db.session.rollback()
            return None

    app.add_member_with_photo = add_member_with_photo

    configure_error_handlers(app)

    with app.app_context():
        # Import models
        from models import User, Member, Page, News

        # Register blueprints
        from blueprints import init_app
        init_app(app)

        # Routes
        @app.route('/')
        def home():
            news = News.query.order_by(News.date_posted.desc()).limit(3).all()
            return render_template('home.html', news=news)

        @app.route('/notre-equipe')
        def team():
            executive_members = [
                {
                    'name': 'M. ABRAHAM MBO',
                    'position': 'Président',
                    'description': 'Expert en investigation privée avec plus de 20 ans d\'expérience.',
                    'photo': 'abraham_mbo.jpg',
                    'linkedin': '#',
                    'email': 'president@cndpepci.ci'
                },
                {
                    'name': 'M. KOFFI YAO CHARLES',
                    'position': 'Vice-Président',
                    'description': 'Spécialiste en sécurité et investigation d\'entreprise.',
                    'photo': 'default.jpg',
                    'linkedin': '#',
                    'email': 'vice-president@cndpepci.ci'
                },
                {
                    'name': 'M. KOUASSI KONAN MARCELIN',
                    'position': 'Secrétaire Général',
                    'description': 'Expert en gestion administrative et coordination.',
                    'photo': 'default.jpg',
                    'email': 'secretariat@cndpepci.ci'
                }
            ]
            
            commissions = [
                {
                    'name': 'Commission Formation',
                    'description': 'Chargée de la formation continue et du développement professionnel des membres.',
                    'icon': 'bi-mortarboard',
                    'members': ['BALLIET Fernand', 'LAGO Hugues', 'DIABY Adams']
                },
                {
                    'name': 'Commission Éthique',
                    'description': 'Veille au respect des règles déontologiques et éthiques de la profession.',
                    'icon': 'bi-shield-check',
                    'members': ['KOUASSI KONAN MARCELIN', 'KOFFI YAO CHARLES']
                },
                {
                    'name': 'Commission Communication',
                    'description': 'Gère la communication externe et les relations publiques.',
                    'icon': 'bi-megaphone',
                    'members': ['ABRAHAM MBO', 'LAGO Hugues']
                },
                {
                    'name': 'Commission Juridique',
                    'description': 'Assure la veille juridique et le conseil légal aux membres.',
                    'icon': 'bi-journal-text',
                    'members': ['DIABY Adams', 'BALLIET Fernand']
                },
                {
                    'name': 'Commission Technique',
                    'description': 'Développe les standards et les bonnes pratiques professionnelles.',
                    'icon': 'bi-gear',
                    'members': ['KOFFI YAO CHARLES', 'KOUASSI KONAN MARCELIN']
                },
                {
                    'name': 'Commission Relations Internationales',
                    'description': 'Développe les partenariats internationaux et la coopération.',
                    'icon': 'bi-globe',
                    'members': ['ABRAHAM MBO', 'DIABY Adams']
                }
            ]
            
            return render_template('team.html', 
                                executive_members=executive_members,
                                commissions=commissions)

        @app.route('/profession/detective')
        def profession_detective():
            return render_template('profession/metier-detective.html', 
                title="Métier de Détective",
                content={
                    'intro': 'Le métier de détective privé en Côte d\'Ivoire',
                    'sections': [
                        {
                            'title': 'Définition et Rôle',
                            'content': 'Le détective privé est un professionnel agréé qui mène des enquêtes pour le compte de particuliers ou d\'entreprises. Son expertise couvre de nombreux domaines : enquêtes civiles, commerciales, numériques et professionnelles.',
                            'icon': 'bi-search'
                        },
                        {
                            'title': 'Compétences Requises',
                            'content': 'Le métier exige des qualités essentielles : discrétion, rigueur, sens de l\'observation, maîtrise des techniques d\'investigation et connaissance du cadre légal.',
                            'icon': 'bi-person-check'
                        },
                        {
                            'title': 'Domaines d\'Intervention',
                            'content': 'Les détectives interviennent dans diverses situations : enquêtes de moralité, recherches de personnes, lutte contre la contrefaçon, intelligence économique, cyber-surveillance...',
                            'icon': 'bi-briefcase'
                        },
                        {
                            'title': 'Cadre Légal',
                            'content': 'L\'exercice de la profession est strictement réglementé. Le détective doit être titulaire d\'une autorisation d\'exercer et respecter un code de déontologie strict.',
                            'icon': 'bi-shield-check'
                        }
                    ]
                })

        @app.route('/client/services')
        def client_services():
            services = [
                {
                    'title': 'Enquêtes Civiles',
                    'description': 'Recherche de personnes, enquêtes familiales, vérifications pré-matrimoniales.',
                    'icon': 'bi-people'
                },
                {
                    'title': 'Enquêtes Commerciales',
                    'description': 'Due diligence, enquêtes de solvabilité, surveillance de la concurrence.',
                    'icon': 'bi-building'
                },
                {
                    'title': 'Sécurité d\'Entreprise',
                    'description': 'Audit de sécurité, protection des données, prévention des fraudes.',
                    'icon': 'bi-shield-lock'
                },
                {
                    'title': 'Cyber-Investigation',
                    'description': 'Analyse numérique, recherche de preuves électroniques, cyber-surveillance.',
                    'icon': 'bi-laptop'
                },
                {
                    'title': 'Protection de la Propriété Intellectuelle',
                    'description': 'Lutte anti-contrefaçon, enquêtes sur les violations de brevets.',
                    'icon': 'bi-file-earmark-text'
                },
                {
                    'title': 'Formation et Conseil',
                    'description': 'Formation en sécurité, conseil en gestion des risques.',
                    'icon': 'bi-mortarboard'
                }
            ]
            return render_template('client/services.html', services=services)

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

        @app.route('/client/faq')
        def client_faq():
            faqs = [
                {
                    'category': 'Questions Générales',
                    'questions': [
                        {
                            'question': 'Qu\'est-ce qu\'un détective privé ?',
                            'answer': 'Un détective privé est un professionnel agréé qui mène des enquêtes privées dans le respect de la loi et de la déontologie.'
                        },
                        {
                            'question': 'Comment choisir un détective privé ?',
                            'answer': 'Vérifiez son agrément officiel, son expérience, ses références et assurez-vous qu\'il est membre d\'une organisation professionnelle reconnue comme la CNDPEPCI.'
                        }
                    ]
                },
                {
                    'category': 'Services et Tarifs',
                    'questions': [
                        {
                            'question': 'Quels types de services proposez-vous ?',
                            'answer': 'Nous proposons des enquêtes civiles, commerciales, numériques, ainsi que des services de protection et de conseil en sécurité.'
                        },
                        {
                            'question': 'Comment sont calculés les honoraires ?',
                            'answer': 'Les honoraires varient selon la nature et la complexité de la mission. Un devis détaillé est établi après étude de votre dossier.'
                        }
                    ]
                },
                {
                    'category': 'Confidentialité et Légalité',
                    'questions': [
                        {
                            'question': 'Les informations sont-elles confidentielles ?',
                            'answer': 'Absolument. Nous sommes tenus au secret professionnel et appliquons des protocoles stricts de confidentialité.'
                        },
                        {
                            'question': 'Les preuves recueillies sont-elles valables en justice ?',
                            'answer': 'Oui, si elles sont obtenues légalement. Nos méthodes respectent strictement le cadre légal pour garantir la recevabilité des preuves.'
                        }
                    ]
                }
            ]
            return render_template('client/faq.html', faqs=faqs)

        @app.route('/formation/programmes')
        def formation_programmes():
            programmes = [
                {
                    'title': 'Formation Initiale en Investigation Privée',
                    'duration': '6 mois',
                    'description': 'Formation complète couvrant les aspects fondamentaux du métier de détective privé.',
                    'modules': [
                        'Cadre juridique et réglementaire',
                        'Techniques d\'investigation',
                        'Surveillance et filature',
                        'Collecte de preuves',
                        'Rédaction de rapports',
                        'Éthique professionnelle'
                    ]
                },
                {
                    'title': 'Formation Continue',
                    'duration': 'Variable',
                    'description': 'Modules de perfectionnement pour les professionnels en exercice.',
                    'modules': [
                        'Nouvelles technologies d\'investigation',
                        'Mise à jour juridique',
                        'Techniques avancées de surveillance',
                        'Cybersécurité pour détectives'
                    ]
                },
                {
                    'title': 'Spécialisations',
                    'duration': '3 mois',
                    'description': 'Formations spécialisées pour des domaines spécifiques.',
                    'modules': [
                        'Investigation d\'entreprise',
                        'Enquêtes numériques',
                        'Protection de la propriété intellectuelle',
                        'Lutte contre la fraude'
                    ]
                }
            ]
            return render_template('formation/programmes.html', programmes=programmes)

        @app.route('/formation/certification')
        def formation_certification():
            certifications = [
                {
                    'title': 'Certification Professionnelle CNDPEPCI',
                    'description': 'La certification officielle requise pour exercer en tant que détective privé.',
                    'requirements': [
                        'Completion de la formation initiale',
                        'Examen théorique',
                        'Évaluation pratique',
                        'Stage professionnel',
                        'Validation du dossier par la commission'
                    ],
                    'validity': '5 ans',
                    'icon': 'bi-award'
                },
                {
                    'title': 'Certifications Spécialisées',
                    'description': 'Certifications pour des domaines d\'expertise spécifiques.',
                    'requirements': [
                        'Certification professionnelle valide',
                        'Formation spécialisée complétée',
                        'Examen spécifique au domaine',
                        'Projet pratique'
                    ],
                    'validity': '3 ans',
                    'icon': 'bi-patch-check'
                },
                {
                    'title': 'Renouvellement de Certification',
                    'description': 'Processus de maintien de la certification professionnelle.',
                    'requirements': [
                        'Formation continue',
                        'Dossier d\'activité',
                        'Mise à jour des connaissances',
                        'Validation par la commission'
                    ],
                    'validity': '5 ans',
                    'icon': 'bi-arrow-repeat'
                }
            ]
            return render_template('formation/certification.html', certifications=certifications)

        @app.route('/formation/calendrier')
        def formation_calendrier():
            events = [
                {
                    'title': 'Formation Initiale - Session 1',
                    'date_start': '15 Janvier 2024',
                    'date_end': '15 Juillet 2024',
                    'location': 'Centre de Formation CNDPEPCI - Abidjan',
                    'status': 'Inscriptions ouvertes',
                    'type': 'formation'
                },
                {
                    'title': 'Examen de Certification',
                    'date_start': '20 Juillet 2024',
                    'date_end': '22 Juillet 2024',
                    'location': 'Siège CNDPEPCI',
                    'status': 'À venir',
                    'type': 'examen'
                },
                {
                    'title': 'Formation Continue - Cybersécurité',
                    'date_start': '5 Août 2024',
                    'date_end': '9 Août 2024',
                    'location': 'En ligne',
                    'status': 'Inscriptions ouvertes',
                    'type': 'formation'
                },
                {
                    'title': 'Formation Spécialisée - Enquêtes d\'entreprise',
                    'date_start': '1 Septembre 2024',
                    'date_end': '30 Novembre 2024',
                    'location': 'Centre de Formation CNDPEPCI - Abidjan',
                    'status': 'Prochainement',
                    'type': 'formation'
                }
            ]
            return render_template('formation/calendrier.html', events=events)

        @app.route('/presse/actualites')
        def presse_actualites():
            actualites = [
                {
                    'title': 'Nouveau cadre réglementaire pour les détectives privés',
                    'date': '15 Décembre 2023',
                    'summary': 'La CNDPEPCI annonce des modifications importantes dans la réglementation des détectives privés.',
                    'image': 'news-1.jpg',
                    'category': 'Réglementation',
                    'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
                },
                {
                    'title': 'Succès de la formation annuelle des détectives',
                    'date': '10 Décembre 2023',
                    'summary': 'Plus de 50 détectives ont participé à la session de formation continue organisée par la CNDPEPCI.',
                    'image': 'news-2.jpg',
                    'category': 'Formation',
                    'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
                },
                {
                    'title': 'Partenariat international pour la lutte contre la fraude',
                    'date': '5 Décembre 2023',
                    'summary': 'La CNDPEPCI signe un accord de collaboration avec des organisations internationales.',
                    'image': 'news-3.jpg',
                    'category': 'Partenariat',
                    'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
                }
            ]
            return render_template('presse/actualites.html', actualites=actualites)

        @app.route('/presse/communiques')
        def presse_communiques():
            communiques = [
                {
                    'title': 'Communiqué officiel : Nouvelles directives pour l\'exercice de la profession',
                    'date': '18 Décembre 2023',
                    'reference': 'COM-2023-001',
                    'content': 'La CNDPEPCI informe tous les détectives privés des nouvelles directives...',
                    'type': 'Important',
                    'attachments': ['directive_2023.pdf']
                },
                {
                    'title': 'Résultats des examens de certification - Session Décembre 2023',
                    'date': '12 Décembre 2023',
                    'reference': 'COM-2023-002',
                    'content': 'Suite aux examens de certification qui se sont tenus...',
                    'type': 'Annonce',
                    'attachments': ['resultats_dec2023.pdf']
                },
                {
                    'title': 'Appel à candidatures : Commission d\'éthique',
                    'date': '8 Décembre 2023',
                    'reference': 'COM-2023-003',
                    'content': 'La CNDPEPCI lance un appel à candidatures pour renouveler...',
                    'type': 'Recrutement',
                    'attachments': []
                }
            ]
            return render_template('presse/communiques.html', communiques=communiques)

        @app.route('/presse/medias')
        def presse_medias():
            medias = [
                {
                    'title': 'Conférence de presse annuelle 2023',
                    'date': '20 Décembre 2023',
                    'type': 'Vidéo',
                    'thumbnail': 'conference-2023.jpg',
                    'duration': '45:30',
                    'description': 'Revue annuelle des activités de la CNDPEPCI',
                    'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
                },
                {
                    'title': 'Interview du Président sur RTI',
                    'date': '15 Décembre 2023',
                    'type': 'Vidéo',
                    'thumbnail': 'interview-president.jpg',
                    'duration': '12:45',
                    'description': 'Le président de la CNDPEPCI présente les nouveaux enjeux de la profession',
                    'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
                },
                {
                    'title': 'Reportage : Dans la peau d\'un détective',
                    'date': '10 Décembre 2023',
                    'type': 'Article',
                    'thumbnail': 'article-detective.jpg',
                    'source': 'Fraternité Matin',
                    'link': 'https://example.com/article',
                    'description': 'Un jour dans la vie d\'un détective privé certifié'
                },
                {
                    'title': 'Album : Cérémonie de remise des certifications',
                    'date': '5 Décembre 2023',
                    'type': 'Photos',
                    'count': 25,
                    'thumbnail': 'ceremonie-2023.jpg',
                    'description': 'Photos de la cérémonie officielle de remise des certifications',
                    'photos': ['photo1.jpg', 'photo2.jpg', 'photo3.jpg', 'photo4.jpg', 'photo5.jpg', 'photo6.jpg']
                }
            ]
            return render_template('presse/medias.html', medias=medias)

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
            members = Member.query.all()
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

        # Routes d'administration
        @app.route('/admin')
        @login_required
        def admin():
            if not current_user.is_admin:
                flash('Accès non autorisé.', 'danger')
                return redirect(url_for('index'))
            members = Member.query.all()
            return render_template('admin/dashboard.html', members=members)

        @app.route('/admin/login', methods=['GET', 'POST'])
        def admin_login():
            if current_user.is_authenticated:
                return redirect(url_for('admin'))
            
            if request.method == 'POST':
                email = request.form.get('email')
                password = request.form.get('password')
                user = User.query.filter_by(email=email).first()
                
                if user and user.check_password(password) and user.is_admin:
                    login_user(user)
                    next_page = request.args.get('next')
                    return redirect(next_page or url_for('admin'))
                flash('Email ou mot de passe incorrect.', 'danger')
            
            return render_template('admin/login.html')

        @app.route('/admin/logout')
        @login_required
        def admin_logout():
            logout_user()
            return redirect(url_for('admin_login'))

        @app.route('/admin/members')
        @login_required
        def admin_members():
            if not current_user.is_admin:
                flash('Accès non autorisé.', 'danger')
                return redirect(url_for('index'))
            members = Member.query.all()
            return render_template('admin/members.html', members=members)

        @app.route('/admin/member/add', methods=['GET', 'POST'])
        @login_required
        def admin_add_member():
            if not current_user.is_admin:
                flash('Accès non autorisé.', 'danger')
                return redirect(url_for('index'))
            
            if request.method == 'POST':
                member_data = {
                    'first_name': request.form.get('first_name'),
                    'last_name': request.form.get('last_name'),
                    'email': request.form.get('email'),
                    'phone': request.form.get('phone'),
                    'agency_name': request.form.get('agency_name'),
                    'role': request.form.get('role'),
                    'region': request.form.get('region'),
                    'license_number': request.form.get('license_number'),
                    'experience_years': int(request.form.get('experience_years', 0)),
                    'domains': request.form.get('domains'),
                    'certifications': request.form.get('certifications'),
                    'website': request.form.get('website')
                }
                
                photo = request.files.get('photo')
                if photo:
                    filename = secure_filename(photo.filename)
                    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    member_data['photo_url'] = filename
                
                try:
                    new_member = Member(**member_data)
                    db.session.add(new_member)
                    db.session.commit()
                    flash('Membre ajouté avec succès!', 'success')
                    return redirect(url_for('admin_members'))
                except Exception as e:
                    flash(f'Erreur lors de l\'ajout du membre: {str(e)}', 'danger')
                    db.session.rollback()
            
            return render_template('admin/add_member.html')

        @app.errorhandler(404)
        def page_not_found(e):
            return render_template('errors/404.html'), 404

        # Initialize database
        with app.app_context():
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