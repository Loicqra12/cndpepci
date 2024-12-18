from app import create_app
from models import db, User

app = create_app()

def create_admin():
    with app.app_context():
        # Vérifier si l'admin existe déjà
        admin = User.query.filter_by(email='admin@cndpepci.ci').first()
        if admin:
            print("L'administrateur existe déjà.")
            return

        # Créer un nouvel administrateur
        admin = User(
            username='admin',
            email='admin@cndpepci.ci',
            is_admin=True
        )
        admin.set_password('Admin@2024')  # Mot de passe par défaut
        
        try:
            db.session.add(admin)
            db.session.commit()
            print("Administrateur créé avec succès!")
            print("\nIdentifiants de connexion :")
            print("----------------------------")
            print("Email : admin@cndpepci.ci")
            print("Mot de passe : Admin@2024")
            print("\nConnectez-vous à : http://127.0.0.1:5000/admin")
        except Exception as e:
            print(f"Erreur lors de la création de l'administrateur : {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    create_admin()
