import os
import sys
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '.env')
load_dotenv(env_path)

# Configuration de l'environnement Python
INTERP = '/home/cp679342p19/virtualenv/3.10.14/3.10/bin/python3.10'
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Configuration des chemins
site_packages = '/home/cp679342p19/virtualenv/3.10.14/3.10/lib/python3.10/site-packages'

# Ajout des chemins au PYTHONPATH
if site_packages not in sys.path:
    sys.path.insert(0, site_packages)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from app import app as application
except Exception as e:
    import logging
    logging.basicConfig(
        filename=os.path.join(current_dir, 'passenger_error.log'),
        level=logging.ERROR,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.error(f"Error importing application: {str(e)}", exc_info=True)
    
    def application(environ, start_response):
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        error_msg = f"Application error: {str(e)}"
        return [error_msg.encode()]
