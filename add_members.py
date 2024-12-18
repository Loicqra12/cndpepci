from app import create_app
from models import db, Member

app = create_app()

members_data = [
    {
        "first_name": "Adams",
        "last_name": "DIABY",
        "email": "contactdetectiveprive@seipci.com",
        "phone": "+225 0554134134",
        "agency_name": "SEIP-CI (Service d'enquête et d'investigation privé de Côte d'Ivoire)",
        "role": "Directeur d'agence",
        "region": "Abidjan",
        "license_number": "N°-SEIP-CI 000/2/2/ABJ1",
        "experience_years": 15,
        "domains": "Intelligence économique, enquêtes privées, surveillance, investigations numériques",
        "photo_url": "adams_diaby.jpg"
    },
    {
        "first_name": "Mamadou",
        "last_name": "OUATTARA",
        "email": "aiicascotedivoire@gmail.com",
        "phone": "+225 0596241111",
        "agency_name": "AIICAS-CI (Agence Internationale d'Investigation Criminelle et d'Analyse Stratégique de Côte d'Ivoire)",
        "role": "Directeur Général d'agence",
        "region": "Bouaké",
        "license_number": "N°-AIICAS-CI-0007/01/10/2024/ABJ",
        "experience_years": 13,
        "certifications": "Formation en Détective Privé (IIDS), École des métiers de sécurité",
        "domains": "Intelligence Économique, Investigation Civile/Économique/Pénale, Filature",
        "photo_url": "photob_oua.png"
    },
    {
        "first_name": "Hugues Bernard",
        "last_name": "LAGO",
        "email": "info@cabinet-eri.com",
        "phone": "+225 01 50 87 55 25",
        "agency_name": "E.R.I (Enquêtes-Recherches-Investigations)",
        "role": "Directeur d'Agence",
        "website": "www.cabinet-eri.com",
        "certifications": "CQP E - ARP de l'ESEP2SE",
        "domains": "Enquêtes, Recherches, Investigations",
        "photo_url": "hugues_lago.jpg"
    },
    {
        "first_name": "Jean Michel",
        "last_name": "HONDÉ",
        "email": "jmhonde@yahoo.fr",
        "phone": "+34 606916668 / +225 07 58 83 74 70",
        "agency_name": "Bureau d'enquête en Espagne et SEIP-CI",
        "region": "Espagne et Abidjan",
        "certifications": "UNED-Madrid (2014-2017): Détective privado-Expert universitaire, IES ATENEA-Ciudad Real (2011-2013): Technicien supérieur",
        "photo_url": "jean_michel_honde.jpg"
    },
    {
        "first_name": "Kouassi Noël",
        "last_name": "YAO",
        "email": "detectivescotedivoire@gmail.com",
        "phone": "0779181502",
        "agency_name": "Compagnie des détectives indépendants",
        "role": "Directeur d'agence",
        "region": "Cocody Angré",
        "license_number": "N°-CDI-CI/0001/AB",
        "experience_years": 9,
        "certifications": "CFMS & Risk Management, NYS-Africa",
        "photo_url": "kouassi_yao.jpg"
    },
    {
        "first_name": "Jean",
        "last_name": "KOUASSI",
        "email": "jean.kouassi@cndpepci.ci",
        "phone": "+225 0708090910",
        "agency_name": "Détective Pro Abidjan",
        "region": "Abidjan",
        "license_number": "CDP001",
        "experience_years": 15,
        "domains": "Enquêtes commerciales",
        "photo_url": None
    }
]

def add_members():
    with app.app_context():
        for member_data in members_data:
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

if __name__ == "__main__":
    add_members()
