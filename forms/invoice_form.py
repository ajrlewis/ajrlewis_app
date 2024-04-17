from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional
from utils.form_mixin import FormMixin

# from models.client import Client


class InvoiceForm(FlaskForm, FormMixin):
    client_id = SelectField("Client", coerce=int, validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    summary = TextAreaField("Summary", validators=[DataRequired()])
    technology = TextAreaField("Technology", validators=[DataRequired()])
    estimated_duration = StringField("Estimated Duration", validators=[DataRequired()])
    estimated_cost = StringField("Estimated Cost", validators=[DataRequired()])
    payment_address = StringField("Payment Address", validators=[DataRequired()])
    date_issued = DateField("Date Issued", default=datetime.utcnow)
    submit = SubmitField("Generate Invoice")
