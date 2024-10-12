from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, SubmitField
from wtforms.validators import Optional

from models.client import Client
from models.invoice import Invoice
from services import client_service
from utils.form_mixin import FormMixin


class InvoiceForm(FlaskForm, FormMixin):
    client_id = SelectField("Client", coerce=int, validators=[Optional()])
    date_min = DateField("Date Minimum", validators=[Optional()])
    date_max = DateField("Date Maximum", validators=[Optional()])
    submit = SubmitField("Add")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        clients = client_service.get_all()
        self.client_id.choices = [(client.client_id, client.name) for client in clients]
