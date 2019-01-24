from application import app, db
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for

from application.project.models import Projekti
from application.project.forms import ProjectForm

@app.route("/project/new/")
@login_required
def project_form():
    return render_template("project/new.html", form = ProjectForm())

@app.route("/project/create/", methods=["POST"])
@login_required
def project_create():
    form = ProjectForm(request.form)

    if not form.validate():
        return render_template("project/new.html", form = form)

    project = Projekti(form.name.data, form.customer.data, form.vakiotyoaika.data)


    db.session().add(project)
    db.session().commit()

    return redirect(url_for("index"))


