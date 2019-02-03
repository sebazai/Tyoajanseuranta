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


@app.route("/project/create/", methods=["POST"])
@login_required(role="ADMIN")
def project_create():
    form = ProjectForm(request.form)

    if not form.validate():
        return render_template("project/new.html", form = form, error = "Varmista, että työaika on kokonaisluku")

    project = Projekti(form.name.data, form.customer.data, form.vakiotyoaika.data)


    db.session().add(project)
    db.session().commit()

    return redirect(url_for("index"))


