from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required

from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text

from application import app, db, login_required
from application.auth.models import User
from application.userproject.models import Userproject
from application.auth.forms import LoginForm, RegistrationForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    #lisää validoinnit

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
    return render_template("auth/registration.html", form = generate_reg_form())

@app.route("/auth/createuser", methods=["POST"])
@login_required(role="ADMIN")
def auth_create_user():
    form = RegistrationForm(request.form)
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
        return render_template("auth/registration.html", form = generate_reg_form(), error = "Käyttäjätunnus varattu, valitse toinen käyttäjätunnus")
    return redirect(url_for("index"))


def generate_reg_form():
    form = RegistrationForm()
    stmt = text("SELECT Projekti.id, Projekti.name FROM Projekti")
    res = db.engine.execute(stmt)
    form.paaprojekti.choices = [(project.id, project.name) for project in res]
    return form
