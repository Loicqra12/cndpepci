from app import app, db
from models import User, Member, ForumTopic, ForumPost, ForumCategory, Page, News

def init_db():
    with app.app_context():
        # Créer toutes les tables
        db.create_all()
        
        # Créer un utilisateur admin par défaut si nécessaire
        if not User.query.filter_by(email='admin@cndpepci.ci').first():
            admin = User(
                username='admin',
                email='admin@cndpepci.ci'
            )
            admin.set_password('votre_mot_de_passe_admin')  # Changez ce mot de passe!
            db.session.add(admin)
        
        # Commit les changements
        db.session.commit()

if __name__ == '__main__':
    init_db()
    print("Base de données initialisée avec succès!")
