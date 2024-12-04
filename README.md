# CNDPEPCI - Système de Gestion des Membres

Application web de gestion des membres pour le Conseil National des Directeurs et Professionnels de l'Immobilier de Côte d'Ivoire (CNDPEPCI).

## Fonctionnalités

- Gestion des membres
- Gestion des actualités
- Gestion des pages de contenu
- Tableau de bord administratif
- Interface responsive

## Technologies utilisées

- Backend : Flask (Python)
- Base de données : SQLite
- Frontend : Bootstrap 5
- Authentification : Flask-Login
- Formulaires : Flask-WTF

## Installation

1. Cloner le repository
```bash
git clone [URL_DU_REPO]
cd cndpepci
```

2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Initialiser la base de données
```bash
flask db upgrade
```

5. Lancer l'application
```bash
flask run
```

## Structure du projet

```
cndpepci/
├── app.py              # Point d'entrée de l'application
├── models.py           # Modèles de données
├── forms.py            # Formulaires
├── extensions.py       # Extensions Flask
├── migrations/         # Migrations de base de données
├── static/            
│   ├── css/           # Fichiers CSS
│   ├── js/            # Fichiers JavaScript
│   └── images/        # Images
└── templates/         # Templates HTML
    ├── admin/         # Templates administrateur
    └── public/        # Templates publics
```

## Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## License

[MIT License](LICENSE)
