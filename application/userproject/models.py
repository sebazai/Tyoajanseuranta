from application import db
from flask_login import login_required, current_user
from application.models import Base

from sqlalchemy.sql import text

class Projekti(Base):
    
    name = db.Column(db.String(144), nullable=False)
    customer = db.Column(db.String(144), nullable=False)
    vakiotyoaika = db.Column(db.Integer, nullable=True)

    def __init__(self, name, customer, vakiotyoaika):
        self.name = name
        self.customer = customer
        self.vakiotyoaika = vakiotyoaika

