from flask import Flask, make_response

app = Flask(__name__)

@app.route('/')
def hello():
    response = make_response('Hello World! Application de test CNDPEP-CI')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/test')
def test():
    return 'Test route working!'

@app.errorhandler(500)
def handle_500(error):
    response = make_response('Erreur Serveur', 500)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

if __name__ == '__main__':
    app.run()
