import datetime

from flask_login import UserMixin

from app import db
from utils.model_mixin import ModelMixin


class User(UserMixin, db.Model, ModelMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), unique=True, nullable=False)
