from app import app
from models import Member, db

def list_all_members():
    with app.app_context():
        members = Member.query.all()
        print("\n=== Liste des membres dans la base de données ===\n")
        if not members:
            print("Aucun membre trouvé dans la base de données.")
        else:
            print(f"Nombre total de membres : {len(members)}\n")
            for member in members:
                print(f"ID: {member.id}")
                print(f"Nom: {member.last_name}")
                print(f"Prénom: {member.first_name}")
                print(f"Email: {member.email}")
                print(f"Téléphone: {member.phone}")
                print(f"Agence: {member.agency_name}")
                print(f"Fonction: {member.role}")
                print(f"Numéro de licence: {member.license_number}")
                print(f"Années d'expérience: {member.experience_years}")
                print(f"Domaines: {member.domains}")
                print("=" * 50)

if __name__ == "__main__":
    list_all_members()
