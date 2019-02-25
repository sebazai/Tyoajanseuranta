from flask_login import current_user
from application import app, db, login_required

from flask import render_template, request, redirect, url_for

from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError

from application.auth.models import get_users_w_project
from application.userproject.models import Userproject
from application.userproject.models import generate_form, paivita_kayttaja, kayttajan_rooli_asiakkaaksi, hae_kirjautuneen_kayttajat_nakyma, tarkista_paaprojekti_ja_vaihda
from application.userproject.forms import UserProjectForm
from application.auth.models import User

@app.route("/userproject/add/")
@login_required(role="ADMIN")
def userproject_form():
    return render_template("userproject/add.html", form = generate_form(), kayttajat = get_users_w_project())

@app.route("/userproject/settings/", methods=["GET", "POST"])
def kayttaja_asetukset():
    if request.method == "GET":
        res = hae_kirjautuneen_kayttajat_nakyma()
        form = generate_form()
        return render_template("userproject/add.html", form = form, kayttajat = res)

@app.route("/userproject/linkuser/", methods=["POST"])
@login_required()
def userproject_create():
    form = UserProjectForm(request.form)
    if request.form['action'] == "Liitä":
        userproject = Userproject(form.asiakas.data)
        userproject.account_id = form.users.data
        userproject.project_id = form.project.data
        if(form.paaprojekti.data == True):
            tarkista_paaprojekti_ja_vaihda(form.users.data)
        if(form.asiakas.data == True):
            kayttajan_rooli_asiakkaaksi(form.users.data)
        userproject.paaprojekti = form.paaprojekti.data
        
        db.session().add(userproject)
        try:
            db.session().commit()
        except IntegrityError:
            db.session.rollback()
            return render_template("userproject/add.html", form = generate_form(), error = "Käyttäjä on jo liitetty projektiin", kayttajat = get_users_w_project())
    elif request.form['action'] == "Päivitä":
        stmt = text("SELECT * FROM userproject WHERE account_id = :accountid AND project_id = :projectid").params(accountid = form.users.data, projectid = form.project.data)
        res = db.engine.execute(stmt)
        row = res.fetchone()
        if row != None:
            res.close()
            tarkista_paaprojekti_ja_vaihda(form.users.data)
            paivita_kayttaja(form.users.data, form.project.data, form.paaprojekti.data, form.asiakas.data)
        else:
            if current_user.role == "ADMIN":
                return render_template("userproject/add.html", form = generate_form(), error = "Liitä käyttäjä ensiksi projektiin.", kayttajat=get_users_w_project())
            else:
                return render_template("userproject/add.html", form = generate_form(), kayttajat = hae_kirjautuneen_kayttajat_nakyma(), error = "Liitä itsesi ensiksi projektiin.")
    if current_user.role == "ADMIN":
        return render_template("userproject/add.html", form = generate_form(), error = 'Käyttäjä liitetty projektiin onnistuneesti!', kayttajat=get_users_w_project())
    return render_template("userproject/add.html", form = generate_form(), kayttajat = hae_kirjautuneen_kayttajat_nakyma(), error = 'Ensisijainen projekti vaihdettu')

