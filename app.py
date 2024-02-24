import sys
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wallet_of_satoshi import WalletOfSatoshi
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
wos = WalletOfSatoshi()

login_manager = LoginManager()
login_manager.login_view = "auth_bp.login"
login_manager.login_message_category = "error"
# login_manager.session_protection = "strong"


def create_app(Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    # Load the configuration
    app.config.from_object(Config)

    # Initialize global
    csrf.init_app(app=app)
    # db.init_app(app=app)
    migrate.init_app(app, db)
    login_manager.init_app(app=app)
    mail.state = mail.init_app(app=app)
    wos.init_app(app=app)

    with app.app_context():
        # TODO (ajrl) Move this to own module:
        @app.context_processor
        def handle_context():
            from datetime import datetime

            return {"now": datetime.utcnow()}

        # Import and register public pages
        from blueprints.public.index_bp import index_bp
        from blueprints.admin.auth_bp import auth_bp

        app.register_blueprint(index_bp, url_prefix="/")
        app.register_blueprint(auth_bp, url_prefix="/auth")

        return app
