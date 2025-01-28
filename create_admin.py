from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash

app = create_app()

def update_admin():
    with app.app_context():
        # Trouver l'admin existant
        admin = User.query.filter_by(username='admin').first()
        if admin:
            # Mettre à jour le mot de passe et l'email
            admin.email = 'admin@cndpepci.org'
            admin.password_hash = generate_password_hash('Cndpepci@2024')
            admin.is_admin = True
            db.session.commit()
            print("Administrateur mis à jour avec succès!")
            print("Email: admin@cndpepci.org")
            print("Mot de passe: Cndpepci@2024")
        else:
            # Créer un nouvel administrateur si aucun n'existe
            new_admin = User(
                username='admin',
                email='admin@cndpepci.org',
                password_hash=generate_password_hash('Cndpepci@2024'),
                is_admin=True
            )
            db.session.add(new_admin)
            db.session.commit()
            print("Nouvel administrateur créé avec succès!")
            print("Email: admin@cndpepci.org")
            print("Mot de passe: Cndpepci@2024")

if __name__ == '__main__':
    update_admin()
