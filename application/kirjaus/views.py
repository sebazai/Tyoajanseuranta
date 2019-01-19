from application import app, db
from flask_login import login_required
from flask import render_template, request, redirect, url_for
from application.kirjaus.models import Kirjaus
from application.kirjaus.forms import KirjausForm
from datetime import datetime, time, date

@app.route("/kirjaus", methods=["GET"])
@login_required
def kirjaus_index():
    return render_template("kirjaus/list.html", kirjauslista = Kirjaus.query.all())

@app.route("/kirjaus/new/")
@login_required
def kirjaus_form():
    return render_template("kirjaus/new.html", form = KirjausForm())

@app.route("/kirjaus/<kirjaus_id>/", methods=["POST"])
@login_required
def kirjaus_uloskirjaus(kirjaus_id):
    kirjaus = Kirjaus.query.get(kirjaus_id)
    now = datetime.datetime.now()
    kirjaus.uloskirjaus = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
    db.session().commit()

    return redirect(url_for("kirjaus_index"))

@app.route("/kirjaus/", methods=["POST"])
@login_required
def kirjaus_create():
    form = KirjausForm(request.form)
    #sisaankirjausPvm = datetime.datetime.strptime(form.aika.data + ' ' + form.time.data, "%Y-%m-%d %H:%M")
    sisaan = datetime.combine(form.aika.data, form.time.data)
    #uloskirjausPvm = datetime.datetime.strptime(form.aika.data + ' ' + form.timeout.data, "%Y-%m-%d %H:%M")
    ulos = datetime.combine(form.aika.data, form.timeout.data)
    kirjaus = Kirjaus(sisaan)
    kirjaus.uloskirjaus = ulos
    db.session().add(kirjaus)
    db.session().commit()
    
    return redirect(url_for("kirjaus_index"))

