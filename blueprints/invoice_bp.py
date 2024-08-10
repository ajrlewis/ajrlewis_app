# Refactor to record_bp (Model, ModelForm)
from io import BytesIO
import datetime

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from flask_login import current_user, login_required
from loguru import logger
from sqlalchemy import desc

from forms.invoice_form import InvoiceForm
from models.client import Client
from models.invoice import Invoice
from utils.invoice_pdf_util import create

invoice_bp = Blueprint("invoice_bp", __name__)


@invoice_bp.route("/", methods=["GET"])
@invoice_bp.route("/<int:invoice_id>", methods=["GET"])
@login_required
def get(invoice_id: int = None):
    logger.debug(f"{invoice_id = }")
    invoice = None
    invoices = None
    invoice_form = InvoiceForm()
    if invoice_id is None:
        invoices = Invoice.query.all()
        for _invoice in invoices:
            client = Client.query.get(_invoice.client_id)
            if client:
                _invoice.client_name = client.name
    else:
        invoice = Invoice.query.get(invoice_id)
        if invoice:
            client = Client.query.get(invoice.client_id)
            invoice.client_name = client.name
            invoice_form.set_data_from_model(invoice)
        else:
            flash(f"Invoice not found.", "error")
    logger.debug(f"{invoice = }")
    return render_template(
        "record.html",
        model="Invoice",
        form=invoice_form,
        form_attributes=[
            "client_id",
            "title",
            "summary",
            "technology",
            "estimated_duration",
            "estimated_cost",
            "payment_address",
            "date_issued",
        ],
        record=invoice,
        records=invoices,
        record_attributes=[
            "client_name",
            "title",
            "summary",
            "technology",
            "estimated_duration",
            "estimated_cost",
            "payment_address",
            "date_issued",
            "reference",
        ],
        downloadable=True,
    )


@invoice_bp.route("/add", methods=["POST"])
@login_required
def add():
    invoice_form = InvoiceForm()
    if invoice_form.validate_on_submit():
        data = invoice_form.data
        invoice = Invoice.add(data)
        flash(f"Invoice added successfully!", "success")
    return redirect(url_for("invoice_bp.get"))


@invoice_bp.route("/update/<int:id>", methods=["POST", "PUT"])
@login_required
def update(id: int):
    invoice = Invoice.query.get(id)
    invoice_form = InvoiceForm()
    if invoice and invoice_form.validate_on_submit():
        user_data = {
            "updated_at": datetime.datetime.now(),
            "updated_by": current_user.id,
        }
        invoice.update(invoice_form.data | user_data)
        flash(f"invoice updated successfully!", "success")
    else:
        flash(f"invoice not found!", "error")
    return redirect(url_for("invoice_bp.get"))


@invoice_bp.route("/delete/<int:id>", methods=["POST", "DELETE"])
@login_required
def delete(id: int):
    invoice = Invoice.query.get(id)
    if invoice:
        invoice.delete()
        flash(f"Invoice deleted successfully!", "success")
    else:
        flash("Invoice not found.", "error")
    return redirect(url_for("invoice_bp.get"))


@invoice_bp.route("/download/<int:id>", methods=["GET"])
@login_required
def download(id: int):
    invoice = Invoice.query.get(id)
    if invoice:
        client = Client.query.get(invoice.client_id)
        invoice.client_name = client.name
        invoice_pdf = create(invoice)
        download_name = f"{invoice.reference}.pdf"
        pdf_file = BytesIO()
        pdf_file.write(invoice_pdf)
        pdf_file.seek(0)
        flash(f"Invoice downloaded successfully!", "success")
        return send_file(
            pdf_file,
            as_attachment=True,
            download_name=download_name,
            mimetype="application/pdf",
        )
    else:
        flash("Invoice not found.", "error")
    return redirect(url_for("invoice_bp.get"))
