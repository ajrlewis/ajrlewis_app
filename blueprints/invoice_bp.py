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
from sqlalchemy import desc
from forms.invoice_form import InvoiceForm
from models.client import Client
from models.invoice import Invoice
from utils import invoice_utils

invoice_bp = Blueprint("invoice_bp", __name__)


@invoice_bp.route("/", methods=["GET"])
@invoice_bp.route("/<int:id>", methods=["GET"])
@login_required
def get(id: int = None):
    invoice = None
    invoices = None
    invoice_form = InvoiceForm()
    if id is None:
        invoices = Invoice.query.all()
        # Merge on client table with client.name
    else:
        invoice = Invoice.query.get(id)
        if invoice:
            invoice_form.set_data_from_model(invoice)
        else:
            flash(f"Invoice not found.", "error")

    return render_template(
        "record.html",
        model="Invoice",
        attributes=[
            "client_id",
            # "client_name",
            "title",
            "summary",
            "technology",
            "estimated_duration",
            "estimated_cost",
            "payment_address",
            "date_issued",
        ],
        form=invoice_form,
        record=invoice,
        records=invoices,
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


@invoice_bp.route("/download/<int:id>", methods=["GET", "POST"])
@login_required
def download(id: int):
    invoice = Invoice.query.get(id)
    if invoice:
        print(f"{invoice = }")
        invoice_pdf = invoice_utils.create(invoice)
        print(f"{invoice_pdf = }")
        # download_name = f"invoice.pdf"
        # pdf_file = BytesIO()
        # pdf_file.write(invoice_pdf)
        # pdf_file.seek(0)
        # flash(f"Invoice downloaded successfully!", "success")
        # return send_file(
        #     pdf_file,
        #     as_attachment=True,
        #     download_name=download_name,
        #     mimetype="application/pdf",
        # )
    else:
        flash("Invoice not found.", "error")
    return redirect(url_for("invoice_bp.get"))
