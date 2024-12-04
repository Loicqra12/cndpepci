from app import app, add_member_with_photo
from models import db

# Préparer les données du membre
member_data = {
    "first_name": "Alex Lorng",
    "last_name": "MBROH",
    "email": "ccinvest.23@gmail.com",
    "phone": "2722281420 / 0545171796 / 0150684248",
    "region": "Abidjan",
    "address": "Angré château",
    "agency_name": "CANAL CONSEILS INVESTIGATIONS (CCI)",
    "role": "Directeur d'Enquête",
    "experience_years": 24,
    "domains": "Enquête privée et familiale,Enquête en entreprises,Collecte d'informations,Investigations foncière",
    "bio": "Ex-Officier Police Judiciaire (OPJ) pendant 22 ans, ARP pendant 2 ans"
}

with app.app_context():
    # Ajouter le membre avec sa photo
    photo_filename = 'WhatsApp Image 2024-12-03 à 22.55.04_d2fb711e.jpg'
    source_photo_path = photo_filename

    member = add_member_with_photo(member_data, photo_filename, source_photo_path)
    print(f"Membre ajouté avec succès. ID: {member.id}")
