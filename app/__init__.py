from flask import Flask
from flask_migrate import Migrate
from config import Config
from .extensions import db, mail
from .google_client import google_oauth
from dotenv import load_dotenv
import os


load_dotenv()
migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True, static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    google_oauth.init_app(app)
    google_oauth.register(
        name='google',
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile',
        }
    )

    with app.app_context():
        from . import routes
        routes.register_routes(app)

    return app
