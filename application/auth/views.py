from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required

from sqlalchemy.exc import IntegrityError

from application import app, db, login_required
from application.auth.models import User
from application.userproject.models import Userproject
from application.project.models import Projekti
from application.kirjaus.models import Kirjaus
from application.auth.forms import LoginForm, RegistrationForm, UpdateForm


@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form, error = "Käyttäjä tai salasana väärin")
    login_user(user)
    return redirect(url_for("index"))


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/register")
@login_required(role="ADMIN")
def auth_register():
    return render_template("auth/registration.html", form = RegistrationForm(), kayttajat = User.query.all())

@app.route("/auth/createuser", methods=["POST"])
@login_required(role="ADMIN")
def auth_create_user():
    form = RegistrationForm(request.form)
    if not form.validate():
        return render_template("auth/registration.html", form = form, kayttajat = User.query.all(), error = "Tarkista syötteet!")
    user = User(form.name.data, form.username.data, form.password.data)
    if form.isadmin.data:
        user.role = "ADMIN"
    else:
        user.role = "USER"
    db.session().add(user)
    
    try:
        db.session().commit()
        #jos lisäys onnistuu, liitetään käyttäjä valittuun projektii
        userproject = Userproject(False)
        userproject.account_id = user.id
        userproject.project_id = form.paaprojekti.data
        userproject.paaprojekti = True
        db.session().add(userproject)
        db.session().commit()
    except IntegrityError:
        db.session().rollback()
        return render_template("auth/registration.html", form = form, error = "Käyttäjätunnus varattu, valitse toinen käyttäjätunnus", kayttajat = User.query.all())
    return redirect(url_for("auth_register"))

@app.route("/auth/update/<account_id>", methods = ["GET", "POST"])
@login_required(role="ADMIN")
def kayttaja_update(account_id):
    if request.method == "GET":
        kayttaja = User.query.get(account_id)
        form = UpdateForm(name = kayttaja.name)
        return render_template("auth/update.html", form = form, kayttaja = kayttaja)
    
    form = UpdateForm(request.form)
    kayttaja = User.query.get(account_id)
    if not form.validate():
        return render_template("auth/update.html", form = form, kayttaja = kayttaja)

    kayttaja.name = form.name.data
    if form.password.data:
        kayttaja.password = form.password.data

    db.session().commit()
    return redirect(url_for('auth_register'))


@app.route("/auth/delete/<account_id>", methods = ["POST"])
@login_required(role="ADMIN")
def kayttaja_poista(account_id):
    Kirjaus.query.filter_by(account_id = account_id).delete()
    Userproject.query.filter_by(account_id = account_id).delete()
    db.session.commit()
    User.query.filter_by(id = account_id).delete()
    db.session.commit()
    return redirect(url_for("auth_register"))

