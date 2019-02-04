from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, BooleanField, SelectField

class LoginForm(FlaskForm):
    username = StringField("Käyttäjätunnus", [validators.Required()])
    password = PasswordField("Salasana", [validators.Required()])

    class Meta:
        csrf = False

class RegistrationForm(FlaskForm):
    username = StringField("Uusi tunnus", [validators.Required()])
    password = PasswordField("Salasana", [validators.Required()])
    name = StringField("Nimi", [validators.Required()])
    paaprojekti = SelectField("Aseta projekti", [validators.optional()])
    isadmin = BooleanField("Pääkäyttäjä")

    class Meta:
        csrf = False

class UpdateForm(FlaskForm):
    name = StringField("Nimi", [validators.Length(min=2, max=144)])
    password = PasswordField("Uusi salasana", [validators.Length(min=5, max=144)])

    class Meta:
        csrf = False
