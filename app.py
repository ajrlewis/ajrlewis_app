import sys

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = "auth_bp.login"
login_manager.login_message_category = "error"


def create_app(Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    csrf.init_app(app=app)
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    login_manager.init_app(app=app)
    mail.state = mail.init_app(app=app)

    with app.app_context():
        from blueprints.index_bp import index_bp
        from blueprints.well_known_bp import well_known_bp

        app.register_blueprint(index_bp, url_prefix="/")
        app.register_blueprint(well_known_bp, url_prefix="/.well-known")

        from blueprints.dashboard.auth_bp import auth_bp
        from blueprints.dashboard.dashboard_bp import dashboard_bp
        from blueprints.dashboard.clients_bp import clients_bp
        from blueprints.dashboard.invoices_bp import invoices_bp
        from blueprints.dashboard.receipts_bp import receipts_bp

        app.register_blueprint(auth_bp, url_prefix="/dashboard/auth")
        app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
        app.register_blueprint(clients_bp, url_prefix="/dashboard/clients")
        app.register_blueprint(invoices_bp, url_prefix="/dashboard/invoices")
        app.register_blueprint(receipts_bp, url_prefix="/dashboard/receipts")

        return app
