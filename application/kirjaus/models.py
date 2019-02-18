from application import db
from flask_login import login_required, current_user
from application.models import Base
from datetime import datetime, date

import os

from sqlalchemy.sql import text

class Kirjaus(Base):
    
    sisaankirjaus = db.Column(db.DateTime, default=db.func.current_timestamp())
    uloskirjaus = db.Column(db.DateTime, nullable=True)
    tehdytminuutit = db.Column(db.Integer, nullable=True)
    kertyma = db.Column(db.Integer, nullable=True)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    userproject_id = db.Column(db.Integer, db.ForeignKey('userproject.id'), nullable=False)

    def __init__(self, sisaankirjaus):
        self.sisaankirjaus = sisaankirjaus

    @staticmethod
    @login_required
    def find_kirjaus_with_null():
        stmt = text("SELECT * FROM Kirjaus WHERE account_id = :accountid AND uloskirjaus IS NULL").params(accountid = current_user.id)

        res = db.engine.execute(stmt)
        palautus = []
        for row in res:
            palautus.append({"id":row[0], "sisaankirjaus":datetime.strftime(row[3] if os.environ.get("HEROKU") else datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S.%f"), "%Y-%m-%d %H:%M:%S"), "uloskirjaus":row[4]})
        return palautus
    @staticmethod
    @login_required
    def get_saldo(userprojektid):
        stmt = text("SELECT SUM(kertyma) FROM Kirjaus WHERE account_id = :accountid AND userproject_id = :userprojekti").params(accountid = current_user.id, userprojekti = userprojektid)
        res = db.engine.execute(stmt)
        for row in res:
            return row[0]

    @staticmethod
    def asiakas_yhteenveto(projekti):
        stmt = text("SELECT SUM(Kirjaus.tehdytminuutit), Account.name, Projekti.name AS projektinimi FROM Kirjaus INNER JOIN Account ON Account.id = Kirjaus.account_id INNER JOIN Userproject ON Userproject.project_id = :projekti AND Userproject.account_id = Kirjaus.account_id AND Kirjaus.userproject_id = Userproject.id INNER JOIN Projekti ON Projekti.id = :projekti GROUP BY Account.name, Projekti.name ORDER BY Account.name ASC").params(projekti = projekti)
        res = db.engine.execute(stmt)
        response = []
        if res.rowcount == 0:
            return response
        else:
            for row in res:
                response.append({"tunnit":(row[0]), "name":row[1], "projekti":row[2]})
            return response
