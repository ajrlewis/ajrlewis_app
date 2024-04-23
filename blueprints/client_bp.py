import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import desc
from forms.client_form import ClientForm
from models.client import Client

client_bp = Blueprint("client_bp", __name__)


@client_bp.route("/", methods=["GET"])
@client_bp.route("/<int:id>", methods=["GET"])
@login_required
def get(id: int = None):
    client = None
    clients = None
    client_form = ClientForm()
    if id is None:
        clients = Client.query.all()
    else:
        client = Client.query.get(id)
        if client:
            client_form.set_data_from_model(client)
        else:
            flash(f"Booking not found.", "error")

    return render_template(
        "record.html",
        model="Client",
        attributes=["name", "domain", "email"],
        form=client_form,
        record=client,
        records=clients,
    )


@client_bp.route("/add", methods=["POST"])
@login_required
def add():
    client_form = ClientForm()
    if client_form.validate_on_submit():
        data = client_form.data
        client = Client.add(data)
        flash(f"Client added successfully!", "success")
    return redirect(url_for("client_bp.get"))


@client_bp.route("/update/<int:id>", methods=["POST", "PUT"])
@login_required
def update(id: int):
    client = Client.query.get(id)
    client_form = ClientForm()
    if client and client_form.validate_on_submit():
        user_data = {
            "updated_at": datetime.datetime.now(),
            "updated_by": current_user.id,
        }
        client.update(client_form.data | user_data)
        flash(f"Client updated successfully!", "success")
    else:
        flash(f"Client not found!", "error")
    return redirect(url_for("client_bp.get"))


@client_bp.route("/delete/<int:id>", methods=["POST", "DELETE"])
@login_required
def delete(id: int):
    client = Client.query.get(id)
    if client:
        client.delete()
        flash(f"Client deleted successfully!", "success")
    else:
        flash("Client not found.", "error")
    return redirect(url_for("client_bp.get"))
