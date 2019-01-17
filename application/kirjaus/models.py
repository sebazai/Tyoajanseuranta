from application import db

class Kirjaus(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sisaankirjaus = db.Column(db.DateTime, default=db.func.current_timestamp())
    uloskirjaus = db.Column(db.DateTime, nullable=True)
    kertyma = db.Column(db.Integer, nullable=False)
    kirjattu_pvm = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, sisaankirjaus):
        self.sisaankirjaus = sisaankirjaus
        self.kertyma = 0

