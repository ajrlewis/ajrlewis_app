import datetime
from app import db
from utils.model_mixin import ModelMixin


class Invoice(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    technology = db.Column(db.Text, nullable=False)

    # service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)
    # service.name
    # service.cost
    # service.duration
    estimated_cost = db.Column(db.String(255), nullable=False)  # e.g. "₿ 0.00 420 069"
    estimated_duration = db.Column(db.String(255), nullable=False)  # e.g. "5 days"

    reference = db.Column(db.String(255), nullable=False)
    date_issued = db.Column(db.DateTime, default=datetime.datetime.now)
    payment_address = db.Column(db.String(42), nullable=False)
    reference = db.Column(db.String(255), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
