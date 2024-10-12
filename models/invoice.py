import datetime

from app import db
from utils.model_mixin import ModelMixin


class Invoice(db.Model, ModelMixin):
    invoice_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    technology = db.Column(db.Text, nullable=False)
    value = db.Column(db.Integer, nullable=False)  # in satoshis
    duration = db.Column(db.Integer, nullable=False)  # in days
    payment_address = db.Column(db.String(42), nullable=False)
    reference = db.Column(db.String(255), nullable=False)
    date_issued = db.Column(db.DateTime, default=datetime.datetime.now)
    reference = db.Column(db.String(255), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("client.client_id"), nullable=False)
    client = db.relationship("Client", backref="invoice")
