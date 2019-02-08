from application import app, db
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for

from application.kirjaus.models import Kirjaus
from application.kirjaus.forms import KirjausForm
from application.userproject.models import Userproject
from application.project.models import Projekti
from application.userproject.views import generate_form

from datetime import datetime, time, date
from sqlalchemy import desc
from sqlalchemy.sql import text, func

@app.route("/kirjaus", methods=["GET"])
@login_required
def kirjaus_index():
    userprojekti = Userproject.query.filter(Userproject.account_id == current_user.id, Userproject.paaprojekti == True).first()
    if userprojekti is None:
        return render_template("userproject/add.html", form = generate_form(), error = "Liitä projektiin, ennen kuin voit kirjata työaikoja")
    projekti = Projekti.query.filter(Projekti.id == userprojekti.project_id).first()
    kirjauslista = Kirjaus.query.filter(Kirjaus.account_id == current_user.id, Kirjaus.userproject_id == userprojekti.id).order_by(desc(Kirjaus.sisaankirjaus)).all()
    saldo = Kirjaus.get_saldo(userprojekti.id)
    if userprojekti.onasiakas is True:
        asiakas = Kirjaus.asiakas_yhteenveto(userprojekti.project_id)
    else:
        asiakas = None
    return render_template("kirjaus/list.html", asiakas = asiakas, kirjauslista = kirjauslista, projekti = projekti.name, saldo = saldo)

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
    kirjaus.tehdytminuutit = minuutit
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
    if kirjaus_sisaan.userproject_id is None:
        return render_template("userproject/add.html", form = generate_form(), error = "Liitä projektiin, ennen kuin voit kirjata työaikoja")
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
    kirjaus.tehdytminuutit = minuutit
    kirjaus.account_id = current_user.id
    projekti = hae_ensisijainen_projekti()
    if projekti is None:
        return render_template("userproject/add.html", form = generate_form(), error = "Liitä projektiin, ennen kuin voit kirjata työaikoja")
    kirjaus.kertyma = laske_kertyma(minuutit, projekti)
    kirjaus.userproject_id = projekti

    db.session().add(kirjaus)
    db.session().commit()
    
    return redirect(url_for("kirjaus_index"))

@login_required
def hae_ensisijainen_projekti():
    stmt = text("SELECT * FROM userproject WHERE account_id = :accountid AND paaprojekti = :true").params(accountid = current_user.id, true = True)
    res = db.session().execute(stmt)
    row = res.first()
    if row is None:
        return None
    projekti = row['id']
    return projekti

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

