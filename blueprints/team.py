from flask import Blueprint, render_template

bp = Blueprint('team', __name__)

@bp.route('/notre-equipe')
def team():
    executive_members = [
        {
            'name': 'M. ABRAHAM MBO',
            'position': 'Président',
            'description': 'Expert en investigation privée avec plus de 20 ans d\'expérience.',
            'photo': 'abraham_mbo.jpg',
            'linkedin': '#',
            'email': 'president@cndpepci.ci'
        },
        {
            'name': 'M. KOFFI YAO CHARLES',
            'position': 'Vice-Président',
            'description': 'Spécialiste en sécurité et investigation d\'entreprise.',
            'photo': 'default.jpg',
            'linkedin': '#',
            'email': 'vice-president@cndpepci.ci'
        },
        {
            'name': 'M. KOUASSI KONAN MARCELIN',
            'position': 'Secrétaire Général',
            'description': 'Expert en gestion administrative et coordination.',
            'photo': 'default.jpg',
            'email': 'secretariat@cndpepci.ci'
        }
    ]
    
    commissions = [
        {
            'name': 'Commission Formation',
            'description': 'Chargée de la formation continue et du développement professionnel des membres.',
            'icon': 'bi-mortarboard',
            'members': ['BALLIET Fernand', 'LAGO Hugues', 'DIABY Adams']
        },
        {
            'name': 'Commission Éthique',
            'description': 'Veille au respect des règles déontologiques et éthiques de la profession.',
            'icon': 'bi-shield-check',
            'members': ['KOUASSI KONAN MARCELIN', 'KOFFI YAO CHARLES']
        },
        {
            'name': 'Commission Communication',
            'description': 'Gère la communication externe et les relations publiques.',
            'icon': 'bi-megaphone',
            'members': ['ABRAHAM MBO', 'LAGO Hugues']
        },
        {
            'name': 'Commission Juridique',
            'description': 'Assure la veille juridique et le conseil légal aux membres.',
            'icon': 'bi-journal-text',
            'members': ['DIABY Adams', 'BALLIET Fernand']
        },
        {
            'name': 'Commission Technique',
            'description': 'Développe les standards et les bonnes pratiques professionnelles.',
            'icon': 'bi-gear',
            'members': ['KOFFI YAO CHARLES', 'KOUASSI KONAN MARCELIN']
        },
        {
            'name': 'Commission Relations Internationales',
            'description': 'Développe les partenariats internationaux et la coopération.',
            'icon': 'bi-globe',
            'members': ['ABRAHAM MBO', 'DIABY Adams']
        }
    ]
    
    return render_template('team.html', 
                        executive_members=executive_members,
                        commissions=commissions)
