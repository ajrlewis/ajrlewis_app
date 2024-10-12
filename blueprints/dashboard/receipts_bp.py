import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from loguru import logger
from sqlalchemy import desc

from forms.receipt_form import ReceiptForm
from models.receipt import Receipt
from app import db

receipts_bp = Blueprint("receipts_bp", __name__)


@receipts_bp.route("/", methods=["GET"])
@login_required
def get_all():
    receipts = db.session.query(Receipt).all()
    receipt_form = ReceiptForm()
    return render_template(
        "dashboard/receipts.html",
        receipts=receipts,
        receipt_form=receipt_form,
        method="post",
    )


@receipts_bp.route("/", methods=["POST"])
# @login_required
def add():
    logger.debug("Adding ...")
    receipt_form = ReceiptForm()
    if receipt_form.validate_on_submit():
        data = receipt_form.data
        logger.debug(f"{data = }")
        data["timestamp"] = datetime.datetime.now()
        receipt = Receipt.add(data)
        logger.debug(f"{receipt = }")
    else:
        logger.error("receipt form did not validate on submit")
        return ""
    return render_template("dashboard/receipt_detail.html", receipt=receipt)


@receipts_bp.route("/<int:receipt_id>", methods=["GET"])
@login_required
def get(receipt_id: int):
    receipt = db.session.query(Receipt).filter_by(receipt_id=receipt_id).first()
    logger.debug(f"{receipt = }")
    return render_template("dashboard/receipt_detail.html", receipt=receipt)


@receipts_bp.route("/<int:receipt_id>/edit", methods=["GET"])
@login_required
def edit(receipt_id: int):
    logger.debug(f"Editing {receipt_id = }")
    receipt = db.session.query(Receipt).filter_by(receipt_id=receipt_id).first()
    logger.debug(f"{receipt = }")
    receipt_form = ReceiptForm.from_model(receipt)
    return render_template(
        "dashboard/receipt_form.html",
        receipt=receipt,
        receipt_form=receipt_form,
        method="put",
    )


@receipts_bp.route("/<int:receipt_id>/download", methods=["GET"])
# @login_required
def download(receipt_id: int):
    logger.debug(f"Downloading {receipt_id = }")
    # return send_file
    return ""


@receipts_bp.route("/<int:receipt_id>", methods=["DELETE"])
# @login_required
def delete(receipt_id: int):
    logger.debug("Deleting ...")
    receipt_form = ReceiptForm()
    if receipt_form.validate_on_submit():
        data = receipt_form.data
        logger.debug(f"{data = }")
        receipt = Receipt.add(data)
        logger.debug(f"{receipt = }")
    else:
        logger.error("receipt form did not validate on submit")
        return ""
    return render_template("dashboard/receipt_detail.html", receipt=receipt)
