from datetime import datetime

from flask_wtf import FlaskForm
from loguru import logger
from wtforms import (
    DateTimeField,
    FloatField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Optional

from app import db
from models.invoice import Invoice
from models.receipt import Receipt
from utils.form_mixin import FormMixin


class ReceiptForm(FlaskForm, FormMixin):
    invoice_id = SelectField("Invoice", coerce=int, validators=[DataRequired()])
    tx_id = StringField("tx_id", validators=[DataRequired()])
    block_time = IntegerField("block_time", validators=[DataRequired()])
    block_height = IntegerField("block_height", validators=[DataRequired()])
    fiat = StringField("fiat", validators=[DataRequired()], default="GBP")
    value_fiat = FloatField("value_fiat", validators=[DataRequired()])

    submit = SubmitField("Add")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        invoices = db.session.query(Invoice).all()
        self.invoice_id.choices = [(i.invoice_id, i.reference) for i in invoices]
