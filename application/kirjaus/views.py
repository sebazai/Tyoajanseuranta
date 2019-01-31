from application import app, db
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for

from application.kirjaus.models import Kirjaus
from application.kirjaus.forms import KirjausForm

from datetime import datetime, time, date
from sqlalchemy import desc
from sqlalchemy.sql import text

@app.route("/kirjaus", methods=["GET"])
@login_required
def kirjaus_index():
    return render_template("kirjaus/list.html", kirjauslista = Kirjaus.query.filter(Kirjaus.account_id == current_user.id).order_by(desc(Kirjaus.sisaankirjaus)).all())

@app.route("/kirjaus/new/")
@login_required
def kirjaus_form():
    return render_template("kirjaus/new.html", form = KirjausForm())

@app.route("/kirjaus/<kirjaus_id>/", methods=["POST"])
@login_required
def kirjaus_uloskirjaus(kirjaus_id):

    kirjaus = Kirjaus.query.get(kirjaus_id)
    now = datetime.now()
    muokattuDatetime = datetime(now.year, now.month, now.day, now.hour, now.minute)
    sisaankirjaus = kirjaus.sisaankirjaus
    minuutit = (int((muokattuDatetime - sisaankirjaus).total_seconds())/60)
    kirjaus.tehdytMinuutit = minuutit
    kirjaus.uloskirjaus = muokattuDatetime;
    kirjaus.kertyma = laske_kertyma(minuutit, kirjaus.userproject_id)
    db.session().commit()

    return redirect(url_for("kirjaus_index"))

@app.route("/kirjaus/delete/<kirjaus_id>", methods=["POST"])
@login_required
def kirjaus_poista(kirjaus_id):
    Kirjaus.query.filter_by(id = kirjaus_id).delete()
    db.session().commit()
    return redirect(url_for("kirjaus_index"))

@app.route("/kirjaus/sisaan", methods=["POST"])
@login_required
def kirjaus_sisaan():
    now = datetime.now()
    kirjaus_sisaan = Kirjaus(datetime(now.year, now.month, now.day, now.hour, now.minute))
    kirjaus_sisaan.account_id = current_user.id
    kirjaus_sisaan.userproject_id = hae_ensisijainen_projekti()
    db.session().add(kirjaus_sisaan)
    db.session().commit()

    return redirect(url_for("kirjaus_index"))

@app.route("/kirjaus/", methods=["POST"])
@login_required
def kirjaus_create():
    form = KirjausForm(request.form)
    if form.timeout.data < form.time.data:
        return render_template("kirjaus/new.html", form = form, error = "Aika ulos ei voi olla pienempi kuin aika sisään")
    if not form.validate():
        return render_template("kirjaus/new.html", form = form)
    
    sisaan = datetime.combine(form.aika.data, form.time.data)
    ulos = datetime.combine(form.aika.data, form.timeout.data)

    minuutit = (int((ulos - sisaan).total_seconds())/60)
            
    kirjaus = Kirjaus(sisaan)
    kirjaus.uloskirjaus = ulos
    kirjaus.tehdytMinuutit = minuutit
    kirjaus.account_id = current_user.id
    projekti = hae_ensisijainen_projekti()
    kirjaus.kertyma = laske_kertyma(minuutit, projekti)
    kirjaus.userproject_id = projekti

    db.session().add(kirjaus)
    db.session().commit()
    
    return redirect(url_for("kirjaus_index"))

@login_required
def hae_ensisijainen_projekti():
    stmt = text("SELECT id FROM userproject WHERE account_id = :accountid AND paaprojekti = 1").params(accountid = current_user.id)
    res = db.session().execute(stmt)
    row = res.fetchone()
    return row['id']

def laske_kertyma(minuutit, userprojekti):
    stmtfirst = text("SELECT project_id FROM userproject WHERE userproject.id = :userproject").params(userproject = userprojekti)
    res2 = db.session().execute(stmtfirst)
    row2 = res2.fetchone()
    stmt = text("SELECT vakiotyoaika FROM projekti WHERE id = :projekti_id").params(projekti_id=row2['project_id'])
    res = db.session().execute(stmt)
    row = res.fetchone()
    vakiotyoaika = row['vakiotyoaika']
    kertyma = minuutit-vakiotyoaika
    return kertyma

