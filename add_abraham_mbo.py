from app import app, add_member_with_photo

# Préparer les données du membre
member_data = {
    "first_name": "Abraham",
    "last_name": "MBO",
    "email": "Détectivesprives@ccrpci.org",
    "phone": "0779794707 / 0103363701",
    "agency_name": "CCRPCI (Cabinet de Conseils et de Recherches Privées de Côte d'Ivoire)",
    "role": "Directeur d'Agence",
    "license_number": "CCRPCI 0005/01/10/2024/ABj",
    "experience_years": 11,
    "domains": "Touts Types de Fraudes,Contrefaçon,Enquêtes privées,Surveillances",
    "certifications": "BSR Lutte contre la Fraude"
}

with app.app_context():
    # Ajouter le membre avec sa photo
    photo_filename = 'WhatsApp Image 2024-12-03 à 22.55.04_d2fb711e.jpg'
    source_photo_path = photo_filename
    
    member = add_member_with_photo(member_data, photo_filename, source_photo_path)
    print(f"Membre ajouté avec succès. ID: {member.id}")
