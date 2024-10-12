import datetime

from flask import Blueprint, render_template, send_file
from flask_login import current_user, login_required
from loguru import logger
from sqlalchemy import desc

from app import db
from services import invoice_service

invoices_bp = Blueprint("invoices_bp", __name__)


@invoices_bp.route("/", methods=["GET"])
@login_required
def get_all():
    invoices = invoice_service.get_all()
    invoice_form = invoice_service.get_form()
    return render_template(
        "dashboard/invoices.html", invoices=invoices, invoice_form=invoice_form
    )


@invoices_bp.route("/filter", methods=["POST"])
@login_required
def get_filtered():
    return render_template(
        "dashboard/invoices.html", invoices=invoices, invoice_form=invoice_form
    )


@invoices_bp.route("/<int:invoice_id>", methods=["GET"])
@login_required
def get(invoice_id: int):
    invoice = invoice_service.get(invoice_id)
    return render_template("dashboard/invoice_detail.html", invoice=invoice)


@invoices_bp.route("/<int:invoice_id>/edit", methods=["GET"])
@login_required
def edit(invoice_id: int):
    invoice = invoice_service.get(invoice_id)
    invoice_form = invoice_service.get_form(invoice)
    return render_template(
        "dashboard/invoice_edit.html", invoice=invoice, invoice_form=invoice_form
    )


@invoices_bp.route("/<int:invoice_id>", methods=["PUT"])
@login_required
def update(invoice_id: int):
    invoice = invoice_service.get(invoice_id)
    invoice_form = InvoiceForm()
    if invoice and invoice_form.validate_on_submit():
        invoice = invoice_service.update(invoice_id, invoice_form.data)
    return render_template("dashboard/invoice_detail.html", invoice=invoice)


@invoices_bp.route("/<int:invoice_id>", methods=["DELETE"])
@login_required
def delete(invoice_id: int):
    invoice_service.delete(invoice_id)
    return ""


@invoices_bp.route("/<int:invoice_id>/download", methods=["GET"])
@login_required
def download(invoice_id: int):
    logger.debug(f"{invoice_id = }")
    pdf_file, download_name = invoice_service.download(invoice_id)
    return send_file(
        pdf_file,
        as_attachment=True,
        download_name=download_name,
        mimetype="application/pdf",
    )


@invoices_bp.route("/", methods=["POST"])
@login_required
def add():
    logger.debug("Adding")
    invoice_form = invoice_service.get_form()
    logger.debug(f"{invoice_form = }")
    if invoice_form.validate_on_submit():
        invoice = invoice_service.add(invoice_form.data)
    else:
        logger.error("invoice form did not validate on submit")
        return ""
    return render_template("dashboard/invoice_detail.html", invoice=invoice)
