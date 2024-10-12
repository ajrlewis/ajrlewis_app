from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional

from utils.form_mixin import FormMixin


class ClientForm(FlaskForm, FormMixin):
    name = StringField("Name", validators=[DataRequired()])
    domain = StringField("Domain", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Add")
