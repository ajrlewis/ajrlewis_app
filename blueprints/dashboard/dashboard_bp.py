from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import desc

dashboard_bp = Blueprint("dashboard_bp", __name__)


@dashboard_bp.route("", methods=["GET"])
@dashboard_bp.route("/", methods=["GET"])
@login_required
def get():
    return render_template("dashboard/dashboard.html")
