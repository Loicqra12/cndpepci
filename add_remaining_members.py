from app import create_app
from models import db, Member

app = create_app()

remaining_members = [
    {
        "first_name": "Fernand",
        "last_name": "BALLIET",
        "email": "direction.cipga.ci@gmail.com",
        "phone": "0576477279 / 0555644162 / 2722450257",
        "website": "www.cipgacotedivoire.com",
        "agency_name": "Cabinet CIPGA CI",
        "role": "Directeur exécutif",
        "license_number": "CP: 1432/PA/56/01",
        "experience_years": 8,
        "certifications": "Détective privé diplômé de ESARP Paris, Intelligence économique et stratégique diplômé IRIS Paris, RCCI diplômé CNPP Vernon, Cyber sécurité certificat du cabinet CEFIS France",
        "domains": "Enquêtes et investigations familiales, Investigations professionnelles, Investigations foncières, Investigations commerciales, Formations et accompagnement, Recherches privées, Cyber sécurité, Dépoussiérage",
        "photo_url": "WhatsApp Image 2024-12-03 à 23.13.29_736f0175.jpg"
    },
    {
        "first_name": "Alex Lorng",
        "last_name": "MBROH",
        "email": "ccinvest.23@gmail.com",
        "phone": "2722281420 / 0545171796 / 0150684248",
        "agency_name": "CANAL CONSEILS INVESTIGATIONS (CCI)",
        "role": "Directeur d'Enquête",
        "region": "Abidjan (Angré château)",
        "experience_years": 24,
        "domains": "Enquête privée et familiale, Enquête en entreprises, Investigations foncière",
        "certifications": "Ex-OPJ pendant 22 ans, ARP pendant 2 ans",
        "photo_url": "WhatsApp Image 2024-12-03 à 22.55.04_d2fb711e.jpg"
    }
]

def add_remaining_members():
    with app.app_context():
        for member_data in remaining_members:
            try:
                # Vérifier si le membre existe déjà
                existing_member = Member.query.filter_by(email=member_data['email']).first()
                if existing_member:
                    print(f"Le membre {member_data['first_name']} {member_data['last_name']} existe déjà.")
                    continue

                # Créer et ajouter le nouveau membre
                new_member = Member(**member_data)
                db.session.add(new_member)
                db.session.commit()
                print(f"Membre {member_data['first_name']} {member_data['last_name']} ajouté avec succès!")
            except Exception as e:
                print(f"Erreur lors de l'ajout de {member_data['first_name']} {member_data['last_name']}: {str(e)}")
                db.session.rollback()

def update_member_photos():
    with app.app_context():
        try:
            # Mise à jour des photos pour chaque membre
            updates = {
                "contactdetectiveprive@seipci.com": "adams_diaby.jpg",
                "aiicascotedivoire@gmail.com": "photob_oua.png",
                "info@cabinet-eri.com": "hugues_lago.jpg",
                "jmhonde@yahoo.fr": "jean_michel_honde.jpg",
                "detectivescotedivoire@gmail.com": "kouassi_yao.jpg",
                "direction.cipga.ci@gmail.com": "WhatsApp Image 2024-12-03 à 23.13.29_736f0175.jpg",
                "ccinvest.23@gmail.com": "WhatsApp Image 2024-12-03 à 22.55.04_d2fb711e.jpg"
            }
            
            for email, photo in updates.items():
                member = Member.query.filter_by(email=email).first()
                if member:
                    member.photo_url = photo
                    print(f"Mise à jour de la photo pour {member.first_name} {member.last_name}")
                else:
                    print(f"Membre avec email {email} non trouvé")
            
            db.session.commit()
            print("Mise à jour des photos terminée")
        except Exception as e:
            print(f"Erreur lors de la mise à jour des photos : {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    add_remaining_members()
    update_member_photos()
