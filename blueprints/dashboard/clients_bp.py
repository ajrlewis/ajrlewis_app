import datetime

from flask import Blueprint, render_template
from flask_login import current_user, login_required
from loguru import logger
from sqlalchemy import desc

from app import db
from forms.client_form import ClientForm
from models.client import Client

clients_bp = Blueprint("clients_bp", __name__)

# client_form = client_service.get_form()
# client_form = client_service.get_form(client)
# client = client_service.get(client_id)
# clients = client_service.get_all()
# clients = client_service.get_filtered()
# client_sevice.update(client, data)
# client_sevice.delete(client)


@clients_bp.route("/", methods=["GET"])
@login_required
def get_all():
    clients = db.session.query(Client).all()
    client_form = ClientForm()
    return render_template(
        "dashboard/clients.html", clients=clients, client_form=client_form
    )


@clients_bp.route("/filter", methods=["POST"])
@login_required
def get_filtered():
    clients = db.session.query(Client).all()
    client_form = ClientForm()
    return render_template(
        "dashboard/clients.html", clients=clients, client_form=client_form
    )


@clients_bp.route("/<int:client_id>", methods=["GET"])
@login_required
def get(client_id: int):
    client = db.session.get(Client, client_id)
    client_form = ClientForm()
    return render_template(
        "dashboard/client_detail.html", client=client, client_form=client_form
    )


@clients_bp.route("/<int:client_id>/edit", methods=["GET"])
@login_required
def edit(client_id: int):
    client = db.session.get(Client, client_id)
    client_form = ClientForm()
    client_form.set_data_from_model(client)
    return render_template(
        "dashboard/client_edit.html", client=client, client_form=client_form
    )


@clients_bp.route("/<int:client_id>", methods=["PUT"])
@login_required
def update(client_id: int):
    client = db.session.get(Client, client_id)
    client_form = ClientForm()
    if client and client_form.validate_on_submit():
        client.update(client_form.data)
    return render_template("dashboard/client_detail.html", client=client)


@clients_bp.route("/<int:client_id>", methods=["DELETE"])
@login_required
def delete(client_id: int):
    client = db.session.get(Client, client_id)
    if client:
        client.delete()
    return ""


def render_oob_template(template: str, div_id: str, **kwargs) -> str:
    rendereds = [
        f'<div hx-swap-oob="afterbegin" id="{div_id}">',
        render_template(template, **kwargs),
        "</div>",
    ]
    rendered = "\n".join(rendereds)
    return rendered


@clients_bp.route("/", methods=["POST"])
@login_required
def add():
    client_form = ClientForm()
    if client_form.validate_on_submit():
        client = Client.add(client_form.data)
    else:
        logger.error("client form did not validate on submit")
        return ""
    oob_rendered = render_oob_template(
        "dashboard/client_detail.html", "clients", client=client
    )
    client_form = ClientForm(formdata=None)
    client_form.name.data = "Foo Bar"
    logger.debug(client_form)
    rendered = render_template("dashboard/client_form.html", client_form=client_form)
    return "\n".join([oob_rendered, rendered]), 200
