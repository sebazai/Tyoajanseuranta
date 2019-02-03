from flask import render_template, url_for, redirect
from application import app

from flask_login import login_required, current_user
from sqlalchemy import and_

from application.kirjaus.models import Kirjaus
from application.kirjaus import views

@app.route("/")
@login_required
def index():
    kirjausaika = Kirjaus.find_kirjaus_with_null()
    if not kirjausaika:
        return render_template("index.html")
    return redirect(url_for("kirjaus_index"))
    

