from application import db
from flask_login import login_required, current_user
from application.models import Base
from application.userproject.forms import UserProjectForm
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import text

class Userproject(Base):
    
    
    __table_args__ = (UniqueConstraint('account_id', 'project_id'),)
    onasiakas = db.Column(db.Boolean, server_default='False',  nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projekti.id'), nullable=False)
    paaprojekti = db.Column(db.Boolean, server_default='False', nullable=False)
    
    
    def __init__(self, asiakas):
        self.onasiakas = asiakas


def paivita_kayttaja(account_id, projekti_id, paaprojekti, asiakas):
    if current_user.role == "ADMIN":
        stmt = text("UPDATE userproject SET paaprojekti = :paaprojekti, onasiakas = :onasiakas WHERE account_id = :tili AND project_id = :projekti").params(paaprojekti = paaprojekti, onasiakas = asiakas, tili = account_id, projekti = projekti_id)
        if (asiakas):
            kayttajan_rooli_asiakkaaksi(account_id)
    else:
        stmt = text("UPDATE userproject SET paaprojekti = :paaprojekti WHERE account_id = :tili AND project_id = :projekti").params(paaprojekti = paaprojekti, tili = account_id, projekti = projekti_id)
    db.engine.execute(stmt)

def kayttajan_rooli_asiakkaaksi(account_id):
    tarkistus = text("SELECT * FROM account WHERE id = :accountid").params(accountid = account_id)
    res = db.engine.execute(tarkistus)
    row = res.fetchone()
    if row.role != "ADMIN":
        stmt2 = text("UPDATE account SET role = 'ASIAKAS' WHERE id = :asiakasid").params(asiakasid = account_id)
        db.engine.execute(stmt2)


def hae_kirjautuneen_kayttajat_nakyma():
    stmt = text("SELECT Account.id, Account.name, Account.username, Projekti.name AS projekti, Userproject.onasiakas, Userproject.paaprojekti FROM account INNER JOIN Userproject ON Userproject.account_id = Account.id INNER JOIN Projekti ON Projekti.id = Userproject.project_id WHERE Account.id = :accountid").params(accountid = current_user.id)
    res = db.session().execute(stmt)
    return res

def tarkista_paaprojekti_ja_vaihda(accountidparam, notthisproject):
    stmt = text("SELECT * FROM userproject WHERE project_id != :notthisproject AND account_id = :accountid AND paaprojekti = :projekti").params(accountid=accountidparam, projekti=True, notthisproject = notthisproject)
    res = db.engine.execute(stmt)
    row = res.fetchone()
    if row != None:
        res.close()
        stmt2 = text("UPDATE userproject SET paaprojekti = :false WHERE account_id = :accountid AND paaprojekti = :projekti").params(false = False, accountid=accountidparam, projekti = True)
        result = db.engine.execute(stmt2)

def generate_form():
    if current_user.role == "ADMIN":
        stmt = text("SELECT Projekti.id, Projekti.name FROM Projekti")
        stmt2 = text("SELECT id, name FROM account")
    else:
        stmt = text("SELECT Projekti.id, Projekti.name FROM Projekti, Userproject WHERE Userproject.project_id = Projekti.id AND Userproject.account_id = :currentuser").params(currentuser = current_user.id)
        stmt2 = text("SELECT id, name FROM account WHERE Account.id = :currentuser").params(currentuser = current_user.id)
    resusers = db.engine.execute(stmt2)
    res = db.engine.execute(stmt)
    form = UserProjectForm()
    form.project.choices = [(project.id, project.name) for project in res]
    form.users.choices = [(user.id, user.name) for user in resusers]
    return form
