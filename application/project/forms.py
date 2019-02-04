from flask_wtf import FlaskForm
from wtforms import validators, widgets
from wtforms import StringField, IntegerField

class ProjectForm(FlaskForm):
   name = StringField("Projektin nimi", [validators.Length(min=2, max=144)])
   customer = StringField("Asiakas", [validators.Length(min=2, max=144)])
   vakiotyoaika = IntegerField("Työaika minuuteissa", [validators.NumberRange(min=0, max=1440)],
                                   widget=widgets.Input(input_type="number"))

   class Meta:
       csrf = False
