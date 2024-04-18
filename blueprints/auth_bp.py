from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from forms.login_form import LoginForm
from models.user import User
from utils.email_utils import send


@login_manager.user_loader
def load_user(user_id: int) -> User:
    return User.query.get(int(user_id))


auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if request.method == "GET":
        return render_template("auth.html", login_form=login_form)
    elif request.method == "POST":
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data
            user = User.query.filter_by(email=email).first()
            if not user or not check_password_hash(user.password, password):
                flash("Please check your login details and try again.", "error")
                return redirect(url_for("auth_bp.login"))
            login_user(user, remember=True)
            next_page = request.form.get("next")
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for("client_bp.get"))
        flash("Please check your login details and try again.", "error")
        return redirect(url_for("auth_bp.login"))


@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("Signed out successfully.", "success")
    return redirect(url_for("auth_bp.login"))
