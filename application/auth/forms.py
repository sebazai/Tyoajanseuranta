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
