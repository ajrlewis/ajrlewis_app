from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Optional

from services import client_service, invoice_service
from utils.form_mixin import FormMixin


class InvoiceForm(FlaskForm, FormMixin):
    client_id = SelectField("Client", coerce=int, validators=[DataRequired()])
    reference = StringField("Reference", validators=[Optional()])
    title = StringField("Title", validators=[DataRequired()])
    summary = TextAreaField("Summary", validators=[DataRequired()])
    technology = TextAreaField("Technology", validators=[DataRequired()])
    duration = IntegerField("Duration / days", validators=[DataRequired()])
    value = IntegerField("Value / satoshis", validators=[DataRequired()])
    payment_address = StringField("Payment Address", validators=[DataRequired()])
    date_issued = DateField("Date Issued", default=datetime.utcnow)
    submit = SubmitField("Add")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        clients = client_service.get_all()
        self.client_id.choices = [(client.client_id, client.name) for client in clients]

    def calculate_reference(self):
        self.title.data = self.title.data.strip()
        self.summary.data = self.summary.data.strip()
        self.technology.data = self.technology.data.strip()
        self.payment_address.data = self.payment_address.data.strip()
        if self.payment_address.data and self.date_issued.data:
            self.reference.data = f"AJRLEWIS-{self.payment_address.data[-8:].upper()}-{self.date_issued.data.strftime('%Y%m%d')}"

    def validate(self, extra_validators=None):
        initial_validation = super(InvoiceForm, self).validate(extra_validators)
        if not initial_validation:
            return False

        self.calculate_reference()
        return True
