from application import db
from flask_login import login_required, current_user
from application.models import Base

class Userproject(Base):
    id = db.Column(db.Integer, primary_key=True)
    onAsiakas = db.Column(db.Boolean, server_default='False',  nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projekti.id'), nullable=False)
    unique_id = db.Column(db.Integer, unique=True, nullable=False)
    paaprojekti = db.Column(db.Boolean, server_default='False', nullable=False)

    def __init__(self, asiakas):
        self.onAsiakas = asiakas

