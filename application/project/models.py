from application import db
from flask_login import login_required, current_user
from application.models import Base

from sqlalchemy.sql import text

class Projekti(Base):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(144), nullable=False)
    customer = db.Column(db.String(144), nullable=False)
    vakiotyoaika = db.Column(db.Integer, nullable=True)

    def __init__(self, name, customer, vakiotyoaika):
        self.name = name
        self.customer = customer
        self.vakiotyoaika = vakiotyoaika

#haetaan käyttäjän ensisijainen projekti
def hae_ensisijainen_projekti():
    stmt = text("SELECT * FROM userproject WHERE account_id = :accountid AND paaprojekti = :true").params(accountid = current_user.id, true = True)
    res = db.session().execute(stmt)
    row = res.first()
    if row is None:
        return None
    projekti = row['id']
    return projekti

# projektilistaus selectfieldiin
def choices_registration_form():
    stmt = text("SELECT Projekti.id, Projekti.name FROM Projekti")
    res = db.engine.execute(stmt)
    return res

