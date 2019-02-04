from application import app, db, login_required
from flask_login import current_user
from flask import render_template, request, redirect, url_for

from application.project.models import Projekti
from application.project.forms import ProjectForm

@app.route("/project/new/")
@login_required(role="ADMIN")
def project_form():
    projektit = Projekti.query.all() 
    return render_template("project/new.html", projektit = projektit, form = ProjectForm())


@app.route("/project/delete/<project_id>", methods=["POST"])
@login_required(role="ADMIN")
def projekti_poista(project_id):
    Projekti.query.filter_by(id = project_id).delete()
    db.session().commit()
    return redirect(url_for("project_form"))

@app.route("/project/update/<project_id>", methods = ["GET", "POST"])
@login_required(role="ADMIN")
def project_update(project_id):
    if request.method == "GET":
        projekti = Projekti.query.get(project_id)
        form = ProjectForm(name = projekti.name, customer = projekti.customer, vakiotyoaika = projekti.vakiotyoaika)
        return render_template("project/update.html", form = form, projekti = projekti)
    
    form = ProjectForm(request.form)
    projekti = Projekti.query.get(project_id)
    if not form.validate():
        return render_template("project/update.html", form = form, projekti = projekti)

    projekti.name = form.name.data
    projekti.customer = form.customer.data
    projekti.vakiotyoaika = form.vakiotyoaika.data

    db.session().commit()
    return redirect(url_for('project_form'))

@app.route("/project/create/", methods=["POST"])
@login_required(role="ADMIN")
def project_create():
    form = ProjectForm(request.form)

    if not form.validate():
        return render_template("project/new.html", form = form, error = "Tarkista syötteet", projektit = Projekti.query.all())

    project = Projekti(form.name.data, form.customer.data, form.vakiotyoaika.data)


    db.session().add(project)
    db.session().commit()

    return redirect(url_for("index"))


