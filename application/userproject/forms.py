from flask_wtf import FlaskForm
from wtforms import validators
from wtforms import StringField, IntegerField, SelectField, BooleanField

from application import db
from sqlalchemy.sql import text

from application.userproject import models
from application.project import models

class UserProjectForm(FlaskForm):
    project = SelectField('Projekti')
    users = SelectField('Käyttäjä')
    asiakas = BooleanField('Onko projektin asiakas?')
    class Meta:
        csrf = False
