from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required

from sqlalchemy.exc import IntegrityError

from application import app, db
from application.auth.models import User
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
@login_required
def auth_register():
    return render_template("auth/registration.html", form = RegistrationForm())

@app.route("/auth/createuser", methods=["POST"])
@login_required
def auth_create_user():
    form = RegistrationForm(request.form)

    if not form.validate():
        return render_template("auth/registration.html", form = form)

    user = User(form.name.data, form.username.data, form.password.data)
    db.session().add(user)

    try:
        db.session().commit()
    except IntegrityError:
        db.session().rollback()
        return render_template("auth/registration.html", form = form, error = "Käyttäjätunnus varattu, valitse toinen käyttäjätunnus")

    return redirect(url_for("index"))
