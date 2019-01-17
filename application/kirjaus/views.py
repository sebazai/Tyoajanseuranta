from application import app, db
from flask import render_template, request, redirect, url_for
from application.kirjaus.models import Kirjaus
import datetime, time

@app.route("/kirjaus", methods=["GET"])
def kirjaus_index():
    return render_template("kirjaus/list.html", kirjauslista = Kirjaus.query.all())

@app.route("/kirjaus/new/")
def kirjaus_form():
    return render_template("kirjaus/new.html")

@app.route("/kirjaus/<kirjaus_id>/", methods=["POST"])
def kirjaus_uloskirjaus(kirjaus_id):
    kirjaus = Kirjaus.query.get(kirjaus_id)
    now = datetime.datetime.now()
    kirjaus.uloskirjaus = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
    db.session().commit()

    return redirect(url_for("kirjaus_index"))

@app.route("/kirjaus/", methods=["POST"])
def kirjaus_create():
    sisaankirjausPvm = datetime.datetime.strptime(request.form.get("aika") + ' ' + request.form.get("time"), "%Y-%m-%d %H:%M")   

    kirjaus = Kirjaus(sisaankirjausPvm)
    db.session().add(kirjaus)
    db.session().commit()
    
    return redirect(url_for("kirjaus_index"))

