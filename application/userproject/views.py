from flask_login import current_user
from application import app, db, login_required

from flask import render_template, request, redirect, url_for

from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError

from application.auth.views import get_users_w_project
from application.userproject.models import Userproject
from application.userproject.forms import UserProjectForm

@app.route("/userproject/add/")
@login_required(role="ADMIN")
def userproject_form():
    return render_template("userproject/add.html", form = generate_form(), kayttajat = get_users_w_project())

def generate_form():
    stmt = text("SELECT Projekti.id, Projekti.name FROM Projekti")
    stmt2 = text("SELECT id, name FROM account")
    resusers = db.engine.execute(stmt2)
    res = db.engine.execute(stmt)
    form = UserProjectForm()
    form.project.choices = [(project.id, project.name) for project in res]
    form.users.choices = [(user.id, user.name) for user in resusers]
    return form

def tarkista_paaprojekti_ja_vaihda(accountidparam):
    stmt = text("SELECT * FROM userproject WHERE account_id = :accountid AND paaprojekti = :projekti").params(accountid=accountidparam, projekti=True)
    res = db.engine.execute(stmt)
    row = res.fetchone()
    if row != None:
        res.close()
        stmt2 = text("UPDATE userproject SET paaprojekti = :false WHERE account_id = :accountid AND paaprojekti = :projekti").params(false = False, accountid=accountidparam, projekti = True)
        result = db.engine.execute(stmt2)


@app.route("/userproject/linkuser/", methods=["POST"])
@login_required(role="ADMIN")
def userproject_create():
    form = UserProjectForm(request.form)
    if request.form['action'] == "Liitä":
        userproject = Userproject(form.asiakas.data)
        userproject.account_id = form.users.data
        userproject.project_id = form.project.data
        if(form.paaprojekti.data == True):
            tarkista_paaprojekti_ja_vaihda(form.users.data)
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
            return render_template("userproject/add.html", form = generate_form(), error = "Liitä käyttäjä ensiksi projektiin.", kayttajat=get_users_w_project())
    return render_template("userproject/add.html", form = generate_form(), error = 'Käyttäjä liitetty projektiin onnistuneesti!', kayttajat=get_users_w_project())


def paivita_kayttaja(account_id, projekti_id, paaprojekti, asiakas):
    stmt = text("UPDATE userproject SET paaprojekti = :paaprojekti, onasiakas = :onasiakas WHERE account_id = :tili AND project_id = :projekti").params(paaprojekti = paaprojekti, onasiakas = asiakas, tili = account_id, projekti = projekti_id)
    db.engine.execute(stmt)

