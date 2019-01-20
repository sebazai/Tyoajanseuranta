from application import db
from flask_login import login_required, current_user
from application.models import Base

from sqlalchemy.sql import text

class Kirjaus(Base):
    
    sisaankirjaus = db.Column(db.DateTime, default=db.func.current_timestamp())
    uloskirjaus = db.Column(db.DateTime, nullable=True)
    tehdytMinuutit = db.Column(db.Integer, nullable=True)
    kertyma = db.Column(db.Integer, nullable=True)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, sisaankirjaus):
        self.sisaankirjaus = sisaankirjaus

    @staticmethod
    @login_required
    def find_kirjaus_with_null():
        stmt = text("SELECT * FROM Kirjaus WHERE account_id = :accountid AND uloskirjaus IS NULL").params(accountid = current_user.id)

        res = db.engine.execute(stmt)
        palautus = []
        for row in res:
            palautus.append({"id":row[0],"sisaankirjaus":row[3], "uloskirjaus":row[4]})
        return palautus
        
