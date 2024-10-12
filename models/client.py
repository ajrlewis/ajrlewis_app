from app import db
from utils.model_mixin import ModelMixin


class Client(db.Model, ModelMixin):
    client_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    domain = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
