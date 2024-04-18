from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import desc
from forms.invoice_form import InvoiceForm

billing_bp = Blueprint("billing_bp", __name__)


@billing_bp.route("/", methods=["GET"])
@login_required
def get():
    invoice_form = InvoiceForm()
    return render_template("billing.html", invoice_form=invoice_form)


@billing_bp.route("/invoice", methods=["GET", "POST"])
@login_required
def invoice():
    invoice_form = InvoiceForm()
    if request.method == "GET":
        return render_template("billing.html", invoice_form=invoice_form)
    elif request.method == "POST":
        print("posting")
        print(invoice_form)
        return render_template("billing.html", invoice_form=invoice_form)


@billing_bp.route("/receipt", methods=["GET", "POST"])
@login_required
def receipt():
    return "", 200
