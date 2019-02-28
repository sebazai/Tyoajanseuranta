from flask_login import current_user
from application import app, db, login_required

from flask import render_template, request, redirect, url_for

from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError

from application.auth.models import get_users_w_project, get_users_per_project
from application.userproject.models import Userproject
from application.userproject.models import generate_form, paivita_kayttaja, kayttajan_rooli_asiakkaaksi, hae_kirjautuneen_kayttajat_nakyma, tarkista_paaprojekti_ja_vaihda
from application.userproject.forms import UserProjectForm
from application.auth.models import User

def get_users_in_project():
    if current_user.role == "ADMIN": 
        raportti = get_users_per_project()
    else:
        raportti = None
    return raportti

def get_add_html_site(message, kayttajat):
    if message == None:
        return render_template("userproject/add.html", raportti = get_users_in_project(), form = generate_form(), kayttajat = kayttajat)
    else:
        return render_template("userproject/add.html", error=message, raportti = get_users_in_project(), form = generate_form(), kayttajat = kayttajat)


@app.route("/userproject/add/")
@login_required(role="ADMIN")
def userproject_form():
    return get_add_html_site(None, get_users_w_project())

@app.route("/userproject/settings/", methods=["GET"])
@login_required()
def kayttaja_asetukset():
    if request.method == "GET":
        res = hae_kirjautuneen_kayttajat_nakyma()
        return get_add_html_site(None, res)

@app.route("/userproject/linkuser/", methods=["POST"])
@login_required(role="ANY")
def userproject_create():
    form = UserProjectForm(request.form)
    if request.form['action'] == "Liitä":
        userproject = Userproject(form.asiakas.data)
        userproject.account_id = form.users.data
        userproject.project_id = form.project.data
        userproject.paaprojekti = form.paaprojekti.data 

        db.session().add(userproject)
        try:
            db.session().commit()

        except IntegrityError:
            db.session.rollback()
            message = "Käyttäjä on jo liitetty projektiin"
            return get_add_html_site(message, get_users_w_project())
        
        if(form.paaprojekti.data == True):
            tarkista_paaprojekti_ja_vaihda(form.users.data, form.project.data)
            paivita_kayttaja(form.users.data, form.project.data, form.paaprojekti.data, form.asiakas.data)
        
        message = "Käyttäjä liitetty projektiin onnistuneesti!"
        return get_add_html_site(message, get_users_w_project())

    elif request.form['action'] == "Päivitä":
        stmt = text("SELECT * FROM userproject WHERE account_id = :accountid AND project_id = :projectid").params(accountid = form.users.data, projectid = form.project.data)
        res = db.engine.execute(stmt)
        row = res.fetchone()
        res.close()
        #jos käyttäjä liitettynä projektiin
        if row != None: 
            tarkista_paaprojekti_ja_vaihda(form.users.data, form.project.data)
            paivita_kayttaja(form.users.data, form.project.data, form.paaprojekti.data, form.asiakas.data)
        else:
            #liitä käyttäjä projektiin
            if current_user.role == "ADMIN":
                message = "Liitä käyttäjä ensiksi projektiin."
                return get_add_html_site(message, get_users_w_project())
            message = "Liitä itsesi ensiksi projektiin."
            return get_add_html_site(message, hae_kirjautuneen_kayttajat_nakyma())
        
        #liitos onnistunut
        if current_user.role == "ADMIN":
            return get_add_html_site('Ensisijainen projekti vaihdettu', get_users_w_project())
        return get_add_html_site('Ensisijainen projekti vaihdettu', hae_kirjautuneen_kayttajat_nakyma())
    

