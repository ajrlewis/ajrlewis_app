from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from loguru import logger
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from forms.login_form import LoginForm
from models.user import User
from utils.email_utils import send


@login_manager.user_loader
def load_user(user_id: int) -> User:
    return db.session.query(User).filter_by(user_id=int(user_id)).first()


auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    logger.error(f"login")
    if request.method == "GET":
        return render_template("dashboard/auth.html", login_form=login_form)
    elif request.method == "POST":
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data
            user = db.session.query(User).filter_by(email=email).first()
            logger.debug(f"{user = }")
            # if not user or not check_password_hash(user.password_hash, password):
            #     flash("Please check your login details and try again.", "error")
            #     logger.error("password not correct")
            #     return redirect(url_for("auth_bp.login"))
            login_user(user, remember=True)
            next_page = request.form.get("next")
            logger.debug(f"{next_page = }")
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for("dashboard_bp.get"))
        logger.error(f"check your login details")
        flash("Please check your login details and try again.", "error")
        return redirect(url_for("auth_bp.login"))


@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("Signed out successfully.", "success")
    return redirect(url_for("auth_bp.login"))
