from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import InputRequired
from wtforms.fields.html5 import DateField, TimeField

class KirjausForm(FlaskForm):
    aika = DateField('Kirjaus', format="%Y-%m-%d", validators=[InputRequired()])
    time = TimeField('Sisään', validators=[InputRequired()])
    timeout = TimeField('Ulos', validators=[InputRequired()])

    class Meta:
        csrf = False
