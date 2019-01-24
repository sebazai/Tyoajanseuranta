from flask_wtf import FlaskForm
from wtforms import validators
from wtforms import StringField, IntegerField

class ProjectForm(FlaskForm):
   name = StringField("Projektin nimi", [validators.Required()])
   customer = StringField("Asiakas", [validators.Required()])
   vakiotyoaika = IntegerField("Työaika minuuteiss", [validators.Required()])

   class Meta:
       csrf = False
