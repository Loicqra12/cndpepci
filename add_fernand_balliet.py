from app import app, add_member_with_photo
from models import db

# Préparer les données du membre
member_data = {
    "first_name": "Fernand",
    "last_name": "BALLIET",
    "email": "direction.cipga.ci@gmail.com",
    "phone": "0576477279 / 0555644162 / 2722450257",
    "website": "www.cipgacotedivoire.com",
    "agency_name": "Cabinet CIPGA CI",
    "role": "Directeur exécutif",
    "license_number": "CP: 1432/PA/56/01",
    "experience_years": 8,
    "domains": "Enquêtes et investigations familiales,Investigations professionnelles,Investigations foncières,Investigations commerciales,Formations et accompagnement,Recherches privées,Cyber sécurité,Dépoussiérage",
    "certifications": "Détective privé diplômé de ESARP Paris,Intelligence économique et stratégique diplômé IRIS Paris,RCCI diplômé CNPP Vernon,Cyber sécurité certificat du cabinet CEFIS France"
}

with app.app_context():
    # Ajouter le membre avec sa photo
    photo_filename = 'WhatsApp Image 2024-12-03 à 23.13.29_736f0175.jpg'
    source_photo_path = photo_filename
    
    member = add_member_with_photo(member_data, photo_filename, source_photo_path)
    print(f"Membre ajouté avec succès. ID: {member.id}")
