from app import create_app
from models import User

app = create_app()

def check_admin():
    with app.app_context():
        admin = User.query.filter_by(email='admin@cndpepci.ci').first()
        if not admin:
            print("L'administrateur n'existe pas dans la base de données!")
            return
        
        print("\nInformations de l'administrateur :")
        print("---------------------------------")
        print(f"Username : {admin.username}")
        print(f"Email : {admin.email}")
        print(f"Is Admin : {admin.is_admin}")
        print(f"Is Active : {admin.is_active}")
        
        # Test du mot de passe
        test_password = 'Admin@2024'
        if admin.check_password(test_password):
            print("\nLe mot de passe est correct!")
        else:
            print("\nLe mot de passe est incorrect!")
            # Réinitialiser le mot de passe
            admin.set_password(test_password)
            from extensions import db
            db.session.commit()
            print("Le mot de passe a été réinitialisé à : Admin@2024")

if __name__ == '__main__':
    check_admin()
