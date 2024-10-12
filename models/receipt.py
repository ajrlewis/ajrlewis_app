import datetime

from app import db
from utils.model_mixin import ModelMixin


class Receipt(db.Model, ModelMixin):
    receipt_id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(
        db.Integer, db.ForeignKey("invoice.invoice_id"), nullable=False, unique=True
    )
    invoice = db.relationship("Invoice", backref="receipt")
    transaction_id = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    block_time = db.Column(db.Integer, nullable=False)
    block_height = db.Column(db.Integer, nullable=False)
    fiat = db.Column(db.String(4), default="GBP", nullable=False)
    value_fiat = db.Column(db.Float, nullable=False)
