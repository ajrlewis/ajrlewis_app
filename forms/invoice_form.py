from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional
from models.client import Client
from utils.form_mixin import FormMixin


class InvoiceForm(FlaskForm, FormMixin):
    client_id = SelectField("Client", coerce=int, validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    summary = TextAreaField("Summary", validators=[DataRequired()])
    technology = TextAreaField("Technology", validators=[DataRequired()])
    estimated_duration = StringField("Estimated Duration", validators=[DataRequired()])
    estimated_cost = StringField("Estimated Cost", validators=[DataRequired()])
    payment_address = StringField("Payment Address", validators=[DataRequired()])
    date_issued = DateField("Date Issued", default=datetime.utcnow)
    submit = SubmitField("Add")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        clients = Client.query.order_by(Client.name).all()
        self.client_id.choices = [(client.id, client.name) for client in clients]
