# Flask käyttöön
from flask import Flask
app = Flask(__name__)

#SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
#tietokanta tuntikirjaus ja tulosta SQL-kyselyt
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tuntikirjaus.db"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

from application import views

from application.kirjaus import models

db.create_all()
