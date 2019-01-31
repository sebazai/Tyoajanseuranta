from application import db
from flask_login import login_required, current_user
from application.models import Base
from datetime import datetime, date

import os

from sqlalchemy.sql import text

class Kirjaus(Base):
    
    sisaankirjaus = db.Column(db.DateTime, default=db.func.current_timestamp())
    uloskirjaus = db.Column(db.DateTime, nullable=True)
    tehdytMinuutit = db.Column(db.Integer, nullable=True)
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
        
