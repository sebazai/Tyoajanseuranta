from application import db
from flask_login import login_required, current_user
from application.models import Base
from sqlalchemy import UniqueConstraint

class Userproject(Base):
    
    
    __table_args__ = (UniqueConstraint('account_id', 'project_id'),)
    onasiakas = db.Column(db.Boolean, server_default='False',  nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projekti.id'), nullable=False)
    paaprojekti = db.Column(db.Boolean, server_default='False', nullable=False)
    
    
    def __init__(self, asiakas):
        self.onAsiakas = asiakas

