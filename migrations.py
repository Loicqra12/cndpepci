from flask_migrate import Migrate
from app import app, db
from models import User, Member, Page, News, ForumCategory, ForumTopic, ForumPost

migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        # Import all models here
        from flask_migrate import upgrade, migrate

        # Create the migrations directory and initialize if it doesn't exist
        migrate.init_app(app, db)
        
        # Create initial migration
        migrate()
        
        # Apply migrations
        upgrade()
