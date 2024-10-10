import sys

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# from flask_wallet_of_satoshi import WalletOfSatoshi
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
# wos = WalletOfSatoshi()

login_manager = LoginManager()
login_manager.login_view = "auth_bp.login"
login_manager.login_message_category = "error"
# login_manager.session_protection = "strong"

# def locale_code_to_name_filter(locale_code: str) -> str:
#     if locale_code == "en_us":
#         return "English (US)"

#     return locale_code
# app.jinja_env.filters['locale_code'] = locale_code_to_name_filter


def create_app(Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    csrf.init_app(app=app)
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    login_manager.init_app(app=app)
    mail.state = mail.init_app(app=app)
    # wos.init_app(app=app)

    with app.app_context():
        from blueprints.index_bp import index_bp
        from blueprints.well_known_bp import well_known_bp
        from blueprints.auth_bp import auth_bp
        from blueprints.dashboard_bp import dashboard_bp
        from blueprints.invoice_bp import invoice_bp
        from blueprints.receipt_bp import receipt_bp
        from blueprints.client_bp import client_bp

        app.register_blueprint(index_bp, url_prefix="/")
        app.register_blueprint(well_known_bp, url_prefix="/.well-known")
        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
        app.register_blueprint(invoice_bp, url_prefix="/dashboard/invoices")
        app.register_blueprint(receipt_bp, url_prefix="/dashboard/receipts")
        app.register_blueprint(client_bp, url_prefix="/dashboard/clients")

        return app
