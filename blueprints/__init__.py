from flask import Blueprint

def init_app(app):
    from .auth import bp as auth_bp
    from .forum import bp as forum_bp
    from . import team
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(forum_bp)
    app.register_blueprint(team.bp)
