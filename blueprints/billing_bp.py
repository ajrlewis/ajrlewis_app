from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import desc
from forms.invoice_form import InvoiceForm

billing_bp = Blueprint("billing_bp", __name__)


@billing_bp.route("/", methods=["GET"])
def get():
    invoice_form = InvoiceForm()
    return render_template("billing.html", invoice_form=invoice_form)


@billing_bp.route("/invoice", methods=["GET", "POST"])
def invoice():
    invoice_form = InvoiceForm()
    if request.method == "GET":
        return render_template("billing.html", invoice_form=invoice_form)
    elif request.method == "POST":
        print("posting")
        print(invoice_form)
        return render_template("billing.html", invoice_form=invoice_form)


@billing_bp.route("/receipt", methods=["GET", "POST"])
def receipt():
    invoice_form = InvoiceForm()
    if request.method == "GET":
        return render_template("billing.html", invoice_form=invoice_form)
    elif request.method == "POST":
        print("posting")
        print(invoice_form)
        return render_template("billing.html", invoice_form=invoice_form)
