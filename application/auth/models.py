from application import db

from application.models import Base
from sqlalchemy.sql import text

class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), unique=True, nullable=False)
    password = db.Column(db.String(144), nullable=False)
    role = db.Column(db.String(144), nullable=False)

    kirjaus = db.relationship("Kirjaus", backref='account', lazy=True)
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def roles(self):
        return self.role


def get_users_w_project():
    stmt = text("SELECT Account.id, Account.name, Account.username, Projekti.name AS projekti, Userproject.onasiakas AS onasiakas, Userproject.paaprojekti FROM account INNER JOIN Userproject ON Userproject.account_id = Account.id INNER JOIN Projekti ON Projekti.id = Userproject.project_id GROUP BY Account.id, Projekti.name, Userproject.onasiakas, Userproject.paaprojekti ORDER BY Account.name ASC")
    res = db.session().execute(stmt)
    return res

def get_users_per_project():
    stmt = text("SELECT COUNT(Account.id) AS maara, Projekti.name AS projekti FROM Account INNER JOIN Userproject ON Userproject.account_id = Account.id AND Userproject.paaprojekti = :true INNER JOIN Projekti ON Projekti.id = Userproject.project_id GROUP BY Projekti.name").params(true = True)
    res = db.session().execute(stmt)
    return res
